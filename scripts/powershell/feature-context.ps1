#!/usr/bin/env pwsh

# Feature context detection utility
# Extracts feature ID from branch name or directory structure

# Function to extract feature ID from current branch name
function Extract-FeatureIdFromBranch {
    try {
        if (Get-Command git -ErrorAction SilentlyContinue) {
            $branchName = git symbolic-ref --short HEAD 2>$null
            if ($LASTEXITCODE -eq 0 -and $branchName -match '^(\d{3})-') {
                return $matches[1]
            }
        }
    } catch {
        # Ignore errors
    }
    return $null
}

# Function to extract feature ID from current directory
function Extract-FeatureIdFromDirectory {
    $currentDir = Get-Location
    $currentPath = $currentDir.Path
    
    # Look for .specify/specs/###-feature-name pattern
    if ($currentPath -match '\\\.specify\\specs\\(\d{3})-') {
        return $matches[1]
    }
    
    # Look for feature directory in parent paths
    $parentDir = $currentPath
    while ($parentDir -and $parentDir -ne "") {
        if ($parentDir -match '\\\.specify\\specs\\(\d{3})-') {
            return $matches[1]
        }
        $parentDir = Split-Path $parentDir -Parent
        if ($parentDir -eq $currentPath) {
            break
        }
    }
    
    return $null
}

# Function to detect feature context and return feature ID
function Detect-FeatureContext {
    # Try branch name first
    $featureId = Extract-FeatureIdFromBranch
    if ($featureId) {
        return $featureId
    }
    
    # Try directory structure
    $featureId = Extract-FeatureIdFromDirectory
    if ($featureId) {
        return $featureId
    }
    
    return $null
}

# Main execution - if called directly, output feature ID
$featureId = Detect-FeatureContext
if ($featureId) {
    Write-Output $featureId
    exit 0
} else {
    exit 1
}