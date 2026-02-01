#!/usr/bin/env python3
"""Test script to run a single bot cycle without the infinite loop"""

from bot import TwitterBot

if __name__ == "__main__":
    print("Running single test cycle...\n")
    bot = TwitterBot()
    bot.run_cycle()
    print("\nTest complete!")
