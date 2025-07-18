import getpass  # To securely get the API key if not set as an environment variable
import os

# Import the components from your newly built library
from cognicoreai import Agent, CalculatorTool, OpenAI_LLM, VolatileMemory


def main():
    """
    An interactive chat session with a CogniCore agent.
    """
    print("--- CogniCore Interactive Chat ---")
    print("This agent is equipped with a calculator tool.")
    print("""Try asking things like 'What is 12 * 5?'
          or just have a normal conversation.""")
    print("Type 'exit' to end the session.\n")

    # --- 1. Set up the API Key ---
    # It's best practice to set this as an environment variable.
    # We check for it, and if not found, we securely ask the user for it.
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY environment variable not found.")
        try:
            api_key = getpass.getpass("Please enter your OpenAI API key: ")
        except Exception as e:
            print(f"Could not read API key: {e}")
            return

    if not api_key:
        print("No API key provided. Exiting.")
        return

    # --- 2. Assemble the Agent's Components ---
    try:
        # Initialize the LLM backend
        llm = OpenAI_LLM(api_key=api_key)

        # Initialize the memory
        memory = VolatileMemory()

        # Gather the tools
        tools = [CalculatorTool()]

    except Exception as e:
        print(f"Failed to initialize agent components: {e}")
        return

    # --- 3. Create the Agent ---
    agent = Agent(
        llm=llm,
        memory=memory,
        tools=tools,
        system_prompt="""You are a friendly and helpful assistant named Cogni.
        You have access to a calculator.""",
    )

    # --- 4. Start the Interactive Loop ---
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Cogni: Goodbye!")
                break

            print("Cogni: Thinking...")
            agent_response = agent.chat(user_input)
            print(f"Cogni: {agent_response}")

        except KeyboardInterrupt:
            print("\nCogni: Session ended by user. Goodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            break


if __name__ == "__main__":
    main()
