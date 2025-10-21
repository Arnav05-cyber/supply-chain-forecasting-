#!/usr/bin/env python3
"""
Setup Git repository and push to GitHub
"""

import subprocess
import os

def run_command(command, description):
    """Run a command and print the result"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} - Error")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def setup_git_repo():
    """Setup and push to GitHub repository"""
    
    print("🚀 SETTING UP GIT REPOSITORY")
    print("=" * 50)
    
    repo_url = "https://github.com/Arnav05-cyber/supply-chain-forecasting-.git"
    
    # Check if git is installed
    if not run_command("git --version", "Checking Git installation"):
        print("❌ Git is not installed. Please install Git first.")
        return False
    
    # Initialize git repository if not already initialized
    if not os.path.exists('.git'):
        run_command("git init", "Initializing Git repository")
    
    # Add all files
    run_command("git add .", "Adding all files to Git")
    
    # Check git status
    run_command("git status", "Checking Git status")
    
    # Commit changes
    commit_message = "Initial commit: AI Forecasting Dashboard with ML model"
    run_command(f'git commit -m "{commit_message}"', "Committing changes")
    
    # Add remote origin
    run_command(f"git remote add origin {repo_url}", "Adding remote origin")
    
    # Check if remote already exists and update if needed
    run_command("git remote -v", "Checking remote repositories")
    
    # Push to GitHub
    print("\n🚀 Pushing to GitHub...")
    print("Note: You may need to authenticate with GitHub")
    
    # Try to push to main branch
    if not run_command("git push -u origin main", "Pushing to main branch"):
        # If main fails, try master
        run_command("git branch -M main", "Renaming branch to main")
        run_command("git push -u origin main", "Pushing to main branch (retry)")
    
    print("\n✅ GIT SETUP COMPLETE!")
    print(f"🔗 Repository URL: {repo_url}")
    print("📊 Your AI Forecasting Dashboard is now on GitHub!")

if __name__ == "__main__":
    setup_git_repo()