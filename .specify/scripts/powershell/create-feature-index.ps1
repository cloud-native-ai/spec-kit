#!/usr/bin/env pwsh

param(
    [switch]$Json
)

# Function to find repository root
function Find-RepoRoot {
    $currentDir = Get-Location
    while ($currentDir -ne $null -and $currentDir.ToString() -ne "") {
        if (Test-Path (Join-Path $currentDir ".git") -PathType Container) {
            return $currentDir
        }
        if (Test-Path (Join-Path $currentDir ".specify") -PathType Container) {
            return $currentDir
        }
        $parent = Split-Path $currentDir -Parent
        if ($parent -eq $currentDir) {
            break
        }
        $currentDir = $parent
    }
    throw "Error: Could not determine repository root. Please run this script from within the repository."
}

# Get repository root
try {
    if (Get-Command git -ErrorAction SilentlyContinue) {
        $repoRoot = git rev-parse --show-toplevel 2>$null
        if ($LASTEXITCODE -eq 0) {
            $hasGit = $true
        } else {
            $repoRoot = Find-RepoRoot
            $hasGit = $false
        }
    } else {
        $repoRoot = Find-RepoRoot
        $hasGit = $false
    }
} catch {
    Write-Error $_.Exception.Message
    exit 1
}

Set-Location $repoRoot

# Create .specify/memory directory if it doesn't exist
$memoryDir = Join-Path $repoRoot ".specify" "memory"
if (-not (Test-Path $memoryDir)) {
    New-Item -ItemType Directory -Path $memoryDir -Force | Out-Null
}
$featuresFile = Join-Path $memoryDir "features.md"

# Function to get current date in YYYY-MM-DD format
function Get-CurrentDate {
    return (Get-Date).ToString("yyyy-MM-dd")
}

# Function to generate short name from feature description
function Generate-ShortName {
    param([string]$description)
    
    $stopWords = @("i", "a", "an", "the", "to", "for", "of", "in", "on", "at", "by", "with", "from", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "should", "could", "can", "may", "might", "must", "shall", "this", "that", "these", "those", "my", "your", "our", "their", "want", "need", "add", "get", "set")
    
    # Convert to lowercase and clean
    $cleanName = $description.ToLower() -replace '[^a-z0-9]', ' ' -replace '\s+', ' '
    $words = $cleanName.Split(' ', [System.StringSplitOptions]::RemoveEmptyEntries)
    
    $meaningfulWords = @()
    foreach ($word in $words) {
        if ($word.Length -eq 0) { continue }
        if ($stopWords -notcontains $word -and ($word.Length -ge 3 -or $description -match "\b$($word.ToUpper())\b")) {
            $meaningfulWords += $word
        }
    }
    
    if ($meaningfulWords.Count -gt 0) {
        $maxWords = [Math]::Min(4, $meaningfulWords.Count)
        $result = $meaningfulWords[0..($maxWords-1)] -join " "
        return $result
    } else {
        # Fallback to first 4 words
        return ($words[0..3] -join " ")
    }
}

# Function to parse existing features
function Parse-ExistingFeatures {
    param([string]$featuresFile)
    
    $existingFeatures = @()
    $nextId = 1
    
    if (-not (Test-Path $featuresFile)) {
        return $existingFeatures, $nextId
    }
    
    $content = Get-Content $featuresFile -Raw
    if ($content -notmatch '\| ID \| Name \| Description \| Status \| Spec Path \| Last Updated \|') {
        return $existingFeatures, $nextId
    }
    
    $lines = Get-Content $featuresFile
    $inTable = $false
    $highestId = 0
    $features = @()
    
    foreach ($line in $lines) {
        if ($line -match '\| ID \| Name \| Description \| Status \| Spec Path \| Last Updated \|') {
            $inTable = $true
            continue
        }
        
        if ($inTable -and $line -match '\|----\|') {
            continue
        }
        
        if ($inTable -and $line -match '^\s*\|\s*\d{3}\s*\|') {
            $parts = $line -split '\|'
            if ($parts.Count -ge 7) {
                $id = ($parts[1] -replace '\s', '')
                $name = ($parts[2] -replace '\s', '')
                $description = ($parts[3] -replace '^\s+|\s+$', '')
                $status = ($parts[4] -replace '\s', '')
                $specPath = ($parts[5] -replace '^\s+|\s+$', '')
                $lastUpdated = ($parts[6] -replace '\s', '')
                
                $features += "$id|$name|$description|$status|$specPath|$lastUpdated"
                
                if ([int]$id -gt $highestId) {
                    $highestId = [int]$id
                }
            }
        }
        
        if ($inTable -and $line -notmatch '^\s*\|') {
            $inTable = $false
        }
    }
    
    return $features, ($highestId + 1)
}

# Function to find spec path
function Find-SpecPath {
    param([string]$featureId, [string]$repoRoot)
    
    $specsDir = Join-Path $repoRoot ".specify" "specs"
    if (Test-Path $specsDir -PathType Container) {
        $pattern = Join-Path $specsDir "$featureId-*"
        $dirs = Get-ChildItem $pattern -Directory -ErrorAction SilentlyContinue
        foreach ($dir in $dirs) {
            $specFile = Join-Path $dir.FullName "spec.md"
            if (Test-Path $specFile -PathType Leaf) {
                $relativePath = $specFile.Substring($repoRoot.Length + 1).Replace('\', '/')
                return $relativePath
            }
        }
    }
    
    return "(Not yet created)"
}

# Function to determine status
function Determine-Status {
    param([string]$specPath)
    
    if ($specPath -eq "(Not yet created)") {
        return "Draft"
    } else {
        return "Planned"
    }
}

# Function to update orphaned features
function Update-OrphanedFeatures {
    param([ref]$featuresRef, [string]$repoRoot)
    
    $updatedFeatures = @()
    foreach ($feature in $featuresRef.Value) {
        $parts = $feature -split '\|'
        if ($parts.Count -ge 6) {
            $id, $name, $description, $status, $specPath, $lastUpdated = $parts
            
            if ($specPath -ne "(Not yet created)" -and $specPath -ne "(Orphaned - spec file deleted)") {
                $fullSpecPath = Join-Path $repoRoot ($specPath.Replace('/', [IO.Path]::DirectorySeparatorChar))
                if (-not (Test-Path $fullSpecPath -PathType Leaf)) {
                    $specPath = "(Orphaned - spec file deleted)"
                }
            }
            
            $updatedFeatures += "$id|$name|$description|$status|$specPath|$lastUpdated"
        }
    }
    
    $featuresRef.Value = $updatedFeatures
}

# Parse existing features
$existingFeatures, $nextId = Parse-ExistingFeatures $featuresFile

# Update orphaned features
Update-OrphanedFeatures ([ref]$existingFeatures) $repoRoot

# Process new feature descriptions from stdin
$newFeatures = @()
if ($input) {
    $input | ForEach-Object {
        if ($_ -ne "") {
            $shortName = Generate-ShortName $_
            $featureId = "{0:d3}" -f $nextId
            $nextId++
            $specPath = Find-SpecPath $featureId $repoRoot
            $status = Determine-Status $specPath
            $lastUpdated = Get-CurrentDate
            $newFeatures += "$featureId|$shortName|$_|$status|$specPath|$lastUpdated"
        }
    }
}

# Combine all features
$allFeatures = $existingFeatures + $newFeatures

# Sort by ID
$sortedFeatures = $allFeatures | Sort-Object { [int]($_ -split '\|')[0] }

# Write features.md
$currentDate = Get-CurrentDate
$totalFeatures = $sortedFeatures.Count

$header = @"
# Project Feature Index

**Last Updated**: $currentDate
**Total Features**: $totalFeatures

## Features

| ID | Name | Description | Status | Spec Path | Last Updated |
|----|------|-------------|--------|-----------|--------------|
"@

Set-Content $featuresFile -Value $header -Encoding UTF8

foreach ($feature in $sortedFeatures) {
    $parts = $feature -split '\|'
    if ($parts.Count -ge 6) {
        $id, $name, $description, $status, $specPath, $lastUpdated = $parts
        Add-Content $featuresFile -Value "| $id | $name | $description | $status | $specPath | $lastUpdated |" -Encoding UTF8
    }
}

# Automatically stage changes if git is available
if ($hasGit) {
    try {
        git add $featuresFile 2>$null
    } catch {
        # Ignore git errors
    }
}

# Output results
if ($Json) {
    Write-Output "{`"FEATURES_FILE`":`"$featuresFile`",`"TOTAL_FEATURES`":$totalFeatures}"
} else {
    Write-Output "FEATURES_FILE: $featuresFile"
    Write-Output "TOTAL_FEATURES: $totalFeatures"
    Write-Output "Feature index created/updated successfully"
}