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
    
    # Check existing features.md table
    if (Test-Path $featuresFile) {
        $content = Get-Content $featuresFile
        foreach ($line in $content) {
            if ($line -match "^\|\s*(\d{3})\s*\|") {
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
    # Convert to lowercase and clean up, limit to 4 words
    return ($Description.ToLower() -replace "[^a-z0-9]", " " -replace "\s+", " ").Trim() -split " " | Select-Object -First 4 | Join-String -Separator " "
}

# Function to extract existing features from the table
function Extract-ExistingFeatures {
    if (Test-Path $featuresFile) {
        $content = Get-Content $featuresFile
        $inTable = $false
        $features = @()
        
        foreach ($line in $content) {
            if ($line -match "^\|\s*ID\s*\|\s*Name\s*\|\s*Description\s*\|\s*Status\s*\|\s*Spec Path\s*\|\s*Last Updated\s*\|$") {
                $inTable = $true
                continue
            }
            
            if ($inTable) {
                if ($line -match "^\|\s*\d{3}\s*\|") {
                    $features += $line
                } elseif ($line -match "^\s*$" -or $line -match "^\|[-\s\|]*\|$") {
                    # Skip empty lines and separator lines
                    continue
                } elseif ($line -match "^\|") {
                    # Still in table, but not a feature row
                    continue
                } else {
                    # End of table
                    break
                }
            }
        }
        
        return $features
    }
    return @()
}

# Create or update the features.md file in Markdown table format
function Create-FeatureIndex {
    param([string]$Description)
    
    $highestNum = Find-HighestFeatureNumber
    $currentNum = $highestNum + 1
    
    # Read existing content if file exists
    $existingHeader = ""
    $existingFeatures = @()
    $existingFooter = ""
    
    if (Test-Path $featuresFile) {
        $content = Get-Content $featuresFile
        $headerEnd = -1
        $tableStart = -1
        $tableEnd = -1
        
        # Find header end (before table)
        for ($i = 0; $i -lt $content.Length; $i++) {
            if ($content[$i] -match "^\|\s*ID\s*\|\s*Name\s*\|\s*Description\s*\|\s*Status\s*\|\s*Spec Path\s*\|\s*Last Updated\s*\|$") {
                $headerEnd = $i - 1
                $tableStart = $i
                break
            }
        }
        
        if ($headerEnd -ge 0) {
            $existingHeader = $content[0..$headerEnd] -join "`n"
        } else {
            # No table found, use all content as header
            $existingHeader = ($content -join "`n") + "`n"
        }
        
        # Extract existing features
        $existingFeatures = Extract-ExistingFeatures
        
        # Find table end and footer
        if ($tableStart -ge 0) {
            $tableEnd = $tableStart
            for ($i = $tableStart + 1; $i -lt $content.Length; $i++) {
                if ($content[$i] -match "^\|\s*\d{3}\s*\|") {
                    $tableEnd = $i
                } elseif ($content[$i] -match "^\s*$" -or $content[$i] -match "^\|[-\s\|]*\|$") {
                    # Skip empty lines and separator lines
                    continue
                } elseif ($content[$i] -match "^\|") {
                    # Still in table
                    $tableEnd = $i
                } else {
                    # End of table, rest is footer
                    $existingFooter = ($content[$i..($content.Length - 1)] -join "`n").Trim()
                    break
                }
            }
        }
    } else {
        # Create default header if file doesn't exist
        $existingHeader = "# Project Feature Index

**Last Updated**: $((Get-Date).ToString("MMMM dd, yyyy"))
**Total Features**: 0

## Features

"
    }
    
    # Generate new content
    $newContent = $existingHeader
    
    # Add table header if this is a new file or if existing file doesn't have table
    $hasTable = $false
    if (Test-Path $featuresFile) {
        $content = Get-Content $featuresFile
        foreach ($line in $content) {
            if ($line -match "^\|\s*ID\s*\|\s*Name\s*\|\s*Description\s*\|\s*Status\s*\|\s*Spec Path\s*\|\s*Last Updated\s*\|$") {
                $hasTable = $true
                break
            }
        }
    }
    
    if (-not $hasTable) {
        $newContent += "| ID | Name | Description | Status | Spec Path | Last Updated |
|----|------|-------------|--------|-----------|--------------|
"
    } elseif (-not (Test-Path $featuresFile)) {
        $newContent += "| ID | Name | Description | Status | Spec Path | Last Updated |
|----|------|-------------|--------|-----------|--------------|
"
    }
    
    # Add existing features
    if ($existingFeatures.Count -gt 0) {
        $newContent += ($existingFeatures -join "`n") + "`n"
    }
    
    # Add new feature from input
    if ($Description -and $Description.Trim() -ne "") {
        $featureName = Generate-FeatureName $Description
        $featureId = "{0:d3}" -f $currentNum
        $today = (Get-Date).ToString("yyyy-MM-dd")
        
        # Check if this feature already exists
        $exists = $false
        if (Test-Path $featuresFile) {
            $content = Get-Content $featuresFile
            $escapedDesc = $Description -replace '[^a-zA-Z0-9]', '.'
            if ($content -match $escapedDesc) {
                $exists = $true
            }
        }
        
        if (-not $exists) {
            # Add new feature row
            $newContent += "| $featureId | $featureName | $Description | Draft | (Not yet created) | $today |
"
            $currentNum++
        }
    }
    
    # Add footer if it exists
    if ($existingFooter -ne "") {
        $newContent += "`n$existingFooter"
    }
    
    # Update total features count and last updated date
    $totalFeatures = ($newContent | Select-String -Pattern "^\|\s*\d{3}\s*\|" -AllMatches).Matches.Count
    $today = (Get-Date).ToString("yyyy-MM-dd")
    $newContent = $newContent -replace "Total Features: \d+", "Total Features: $totalFeatures"
    $newContent = $newContent -replace "Last Updated: \d{4}-\d{2}-\d{2}", "Last Updated: $today"
    $newContent = $newContent -replace "Last Updated: [A-Z][a-z]* \d{1,2}, \d{4}", "Last Updated: $((Get-Date).ToString("MMMM dd, yyyy"))"
    
    Set-Content -Path $featuresFile -Value $newContent -Encoding UTF8
    
    # Automatically stage changes if git is available
    try {
        $gitPath = Get-Command git -ErrorAction SilentlyContinue
        if ($gitPath) {
            git add $featuresFile 2>$null
        }
    } catch {
        # Ignore git errors
    }
    
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

| ID | Name | Description | Status | Spec Path | Last Updated |
|----|------|-------------|--------|-----------|--------------|

"
        Set-Content -Path $featuresFile -Value $emptyContent -Encoding UTF8
    } else {
        # Update last updated date
        $content = Get-Content $featuresFile
        $content = $content -replace "Last Updated: .*", "Last Updated: $((Get-Date).ToString("MMMM dd, yyyy"))"
        Set-Content -Path $featuresFile -Value ($content -join "`n") -Encoding UTF8
    }
    
    # Count existing features
    $totalFeatures = 0
    if (Test-Path $featuresFile) {
        $content = Get-Content $featuresFile
        $totalFeatures = ($content | Where-Object { $_ -match "^\|\s*\d{3}\s*\|" }).Count
    }
    
    # Automatically stage changes if git is available
    try {
        $gitPath = Get-Command git -ErrorAction SilentlyContinue
        if ($gitPath) {
            git add $featuresFile 2>$null
        }
    } catch {
        # Ignore git errors
    }
    
    if ($Json) {
        Write-Output (@{FEATURES_FILE=$featuresFile; TOTAL_FEATURES=$totalFeatures} | ConvertTo-Json)
    } else {
        Write-Host "FEATURES_FILE: $featuresFile"
        Write-Host "TOTAL_FEATURES: 0"
        Write-Host "Feature index initialized (no new features added)"
    }
} else {
    Create-FeatureIndex $FeatureDescription
}