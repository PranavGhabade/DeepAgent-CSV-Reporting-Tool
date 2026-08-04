from dotenv import load_dotenv

from core.orchestrator import Orchestrator

load_dotenv()

# Initialize

orchestrator = Orchestrator()

# Load Dataset

orchestrator.set_dataset("sample_data/test_1.csv")

print("\n" + "=" * 60)
print("         ABC Analytics CSV Reporting Tool")
print("=" * 60)
print("Dataset Loaded Successfully.")
print("Dataset : sample_data/test.csv")

# Main Menu

while True:

    print("\n" + "-" * 60)
    print("1. Generate Complete Report")
    print("2. Ask Dataset Query")
    print("3. Exit")
    print("-" * 60)

    choice = input("Enter your choice: ").strip()

    # Generate Report

    if choice == "1":

        print("\nGenerating Report...\n")

        orchestrator.generate_report()

        print("\n" + "=" * 60)
        print("Report Generated Successfully")
        print("=" * 60)

        print("Markdown Report : outputs/report.md")
        print("PDF Report      : outputs/report.pdf")
        print("Charts Folder   : outputs/charts")

        input("\nPress Enter to return to the Main Menu...")

    # Ask Query

    elif choice == "2":

        while True:

            query = input("\nEnter your query:\n> ").strip()

            if not query:
                print("Please enter a valid query.")
                continue

            print("\nProcessing your request...\n")

            answer = orchestrator.answer_query(query)

            print("\n" + "=" * 60)
            print("RESULT")
            print("=" * 60)

            print(answer)

            print("\n" + "-" * 60)
            print("1. Ask Another Query")
            print("2. Return to Main Menu")
            print("-" * 60)

            option = input("Choice: ").strip()

            if option != "1":
                break

    # Exit

    elif choice == "3":

        print("\nThank you for using ABC Analytics CSV Reporting Tool.")
        break

    # Invalid Option

    else:

        print("\nInvalid choice. Please try again.")