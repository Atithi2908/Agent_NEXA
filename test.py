from voice.manager import VoiceManager


def main():

    voice = VoiceManager()

    print("=" * 40)
    print("NEXA Voice Test")
    print("=" * 40)

    while True:

        print("\nPress Enter to speak...")
        input()

        goal = voice.listen()

        print(f"\nYou said: {goal}")

        if goal.lower() in [
            "exit",
            "quit",
            "stop"
        ]:

            voice.speak(
                "Goodbye!"
            )

            break

        voice.speak(
            f"You said: {goal}"
        )


if __name__ == "__main__":
    main()