#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#  file:    git.py
#  version: 1.0
#  date:    30.09.2017
#  author:  Bernard Tsai (bernard@tsai.eu)
#  description:
#    This script allows to sync with a remote repository.
# ------------------------------------------------------------------------------

import argparse
import os
import shutil
import subprocess

# ------------------------------------------------------------------------------

class Git():

    def __init__(self, path, repo):
        """Initialize local repository with contents of the remote repository"""
        self.encoding  = "utf-8"
        self.path      = path
        self.repo      = repo
        self.directory = ""

        # ensure that path exists and clone the repos
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        # cleanup tree
        self.cleanup()

        # clone
        self.clone()

    def cleanup(self):
        """Remove all contents of directory"""

        # check if the directory exists
        if not os.path.exists(self.path):
            return

        # check if the directory is a directory
        if not os.path.isdir(self.path):
            return

        # loop over content of directory and remove it
        for the_file in os.listdir(self.path):
            file_path = os.path.join(self.path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                pass

    def clone(self):
        """Clone remote repository to local directory"""
        out, err, code = self.command( ["git", "clone", self.repo] )

        # find the directory into which the
        self.directory = self.path
        for path in os.listdir(self.path):
            self.directory = os.path.join(self.path,path)
            break

    def write(self,path,content):
        """Write content to a file with local directory"""
        file_path = os.path.join( self.directory, path)
        with open(file_path, "w")  as file:
            file.write( content )

    def add(self,path):
        """Add file to changeset"""
        out, err, code = self.command( ["git", "add", path], self.directory )

    def commit(self,message):
        """Commit change set"""
        out, err, code = self.command( ["git", "commit", "-m", message], self.directory )

    def push(self):
        """Sync remote repository with contents of local directory"""
        out, err, code = self.command( ["git", "push"], self.directory )

    def command(self,cmd,directory=None):
        """Execute a command"""
        if not directory:
            directory = self.path

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=directory)

        out, err = process.communicate()
        out      = out.decode(self.encoding)
        err      = err.decode(self.encoding)

        code = process.poll()

        return out, err, code

# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------
def main():
    # setup command line parser
    parser = argparse.ArgumentParser(
        prog        = "git.py",
        description = "Clones a remote repository to a local directory",
    )
    parser.add_argument("-p", "--path", required=True, type=str, help="local directory")
    parser.add_argument("-r", "--repo", required=True, type=str, help="url of the remote repository")
    args = parser.parse_args()

    # execute sample program
    # git = Git( args.path, args.repo )
    # git.write( "test.txt", "Hello World" )
    # git.add(   "test.txt" )
    # git.commit( "Initial commit" )
    # git.push()

# ----- MAIN -------------------------------------------------------------------

if __name__ == '__main__':
    main()
