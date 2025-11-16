<#
.SYNOPSIS
    Create or update the project-level feature index based on high-level goals or existing context.

.DESCRIPTION
    This script creates or updates a features.md file in the project root that serves as the
    single source of truth for all project features and their current status.

.PARAMETER Json
    Output results in JSON format instead of human-readable format.

.PARAMETER FeatureDescription
    Feature description to add to the feature index.

.EXAMPLE
    .\create-feature-index.ps1 -FeatureDescription "Add user authentication system"
    
.EXAMPLE
    .\create-feature-index.ps1 -Json -FeatureDescription "Implement OAuth2 integration for API"
#>

param(
    [switch]$Json,
    [string]$FeatureDescription
)

# Find repository root
$repoRoot = $null
$currentPath = $PSScriptRoot
while ($currentPath -and $currentPath -ne "") {
    if (Test-Path (Join-Path $currentPath ".git") -PathType Container -or 
        Test-Path (Join-Path $currentPath ".specify") -PathType Container) {
        $repoRoot = $currentPath
        break
    }
    $currentPath = Split-Path $currentPath -Parent
}

if (-not $repoRoot) {
    Write-Error "Could not determine repository root. Please run this script from within the repository."
    exit 1
}

Set-Location $repoRoot

$featuresFile = Join-Path $repoRoot "features.md"

# Function to find the highest existing feature number
function Find-HighestFeatureNumber {
    $highest = 0
    
    # Check existing features.md
    if (Test-Path $featuresFile) {
        $content = Get-Content $featuresFile
        foreach ($line in $content) {
            if ($line -match "### Feature (\d+):") {
                $num = [int]$matches[1]
                if ($num -gt $highest) { $highest = $num }
            }
        }
    }
    
    # Check existing spec directories
    $specsDir = Join-Path $repoRoot ".specify" "specs"
    if (Test-Path $specsDir) {
        $dirs = Get-ChildItem $specsDir -Directory
        foreach ($dir in $dirs) {
            if ($dir.Name -match "^(\d+)-") {
                $num = [int]$matches[1]
                if ($num -gt $highest) { $highest = $num }
            }
        }
    }
    
    return $highest
}

# Function to generate a clean feature name from description
function Generate-FeatureName {
    param([string]$Description)
    return ($Description.ToLower() -replace "[^a-z0-9]", " " -replace "\s+", " ").Trim() -replace " ", "-"
}

# Create or update the features.md file
function Create-FeatureIndex {
    param([string]$Description)
    
    $highestNum = Find-HighestFeatureNumber
    $currentNum = $highestNum + 1
    
    # Read existing content if file exists
    $existingContent = ""
    $existingFeatures = @()
    if (Test-Path $featuresFile) {
        $existingContent = Get-Content $featuresFile -Raw
        # Extract existing feature entries
        $lines = $existingContent -split "`n"
        foreach ($line in $lines) {
            if ($line -match "^### Feature (\d+):") {
                $existingFeatures += $matches[1]
            }
        }
    }
    
    # Generate new content
    $newContent = "# Project Feature Index

**Last Updated**: $((Get-Date).ToString("MMMM dd, yyyy"))
**Total Features**: TBD

## Features
"
    
    # Add existing features first (but only the feature entries, not the header)
    if ($existingContent -ne "") {
        if ($existingContent -match "(?s)## Features.*") {
            $featuresSection = $matches[0]
            # Remove the header line and keep only the content
            $featuresContent = ($featuresSection -split "`n" | Select-Object -Skip 1) -join "`n"
            if ($featuresContent.Trim() -ne "") {
                $newContent += $featuresContent
            }
        }
    }
    
    # Add new feature from input
    if ($Description -and $Description.Trim() -ne "") {
        $featureName = Generate-FeatureName $Description
        $featureId = "{0:d3}" -f $currentNum
        
        # Check if this feature already exists
        $exists = $false
        if (Test-Path $featuresFile) {
            if (Select-String -Path $featuresFile -Pattern ([regex]::Escape($Description)) -Quiet) {
                $exists = $true
            }
        }
        
        if (-not $exists) {
            $truncatedDesc = if ($Description.Length -gt 50) { $Description.Substring(0, 50) + "..." } else { $Description }
            $newContent += "

### Feature $featureId: $truncatedDesc
- **Status**: Draft
- **Description**: $Description
- **Specification**: (Not yet created)
- **Key Acceptance Criteria**: (To be defined in specification)
"
            $currentNum++
        }
    }
    
    # Update total features count
    $totalFeatures = ([regex]::Matches($newContent, "^### Feature ")).Count
    $newContent = $newContent -replace "Total Features: TBD", "Total Features: $totalFeatures"
    
    Set-Content -Path $featuresFile -Value $newContent -Encoding UTF8
    
    if ($Json) {
        Write-Output (@{FEATURES_FILE=$featuresFile; TOTAL_FEATURES=$totalFeatures} | ConvertTo-Json)
    } else {
        Write-Host "FEATURES_FILE: $featuresFile"
        Write-Host "TOTAL_FEATURES: $totalFeatures"
        Write-Host "Feature index created/updated successfully"
    }
}

# Main execution
if (-not $FeatureDescription) {
    # No input provided, just ensure features.md exists or create empty one
    if (-not (Test-Path $featuresFile)) {
        $emptyContent = "# Project Feature Index

**Last Updated**: $((Get-Date).ToString("MMMM dd, yyyy"))
**Total Features**: 0

## Features

"
        Set-Content -Path $featuresFile -Value $emptyContent -Encoding UTF8
    }
    
    if ($Json) {
        Write-Output (@{FEATURES_FILE=$featuresFile; TOTAL_FEATURES=0} | ConvertTo-Json)
    } else {
        Write-Host "FEATURES_FILE: $featuresFile"
        Write-Host "TOTAL_FEATURES: 0"
        Write-Host "Feature index initialized (no new features added)"
    }
} else {
    Create-FeatureIndex $FeatureDescription
}