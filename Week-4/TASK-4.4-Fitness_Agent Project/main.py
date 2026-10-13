"""
Perfect Fitness Agent - Main Application Interface
Menu-based interface for seamless interaction
"""

import sys
from simple_fitbuddy import main as simple_main


def print_welcome():
    """Print welcome message"""
    print("\n" + "="*70)
    print("  Perfect Fitness Agent - Your AI Health Assistant")
    print("="*70)
    print("\nCapstone Project: AI Agent System")
    print("Features:")
    print("  * RAG (Retrieval from health knowledge base)")
    print("  * Tool Use (7 intelligent health calculators)")
    print("  * Multi-step Reasoning (chained calculations)")
    print("  * Seamless Menu Interface")
    print("  * No API Key Required")
    print("\nI can help you with:")
    print("  * BMI calculation and health analysis")
    print("  * Daily calorie needs and meal planning")
    print("  * Water intake recommendations")
    print("  * Sleep requirements by age")
    print("  * Target heart rate zones")
    print("  * Fitness and nutrition guidance")
    print("  * Mental health and stress management")
    print("\nType 'quit' or 'exit' to end the conversation.")
    print("="*70 + "\n")


def main():
    """Main application - runs menu-based interface"""
    print_welcome()
    print("Using menu-based interface for seamless interaction...\n")
    simple_main()


if __name__ == "__main__":
    main()
