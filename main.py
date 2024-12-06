import click
from assistant import query_model
from knowledge_base import load_knowledge_base
from conversation import extract_knowledge, update_knowledge_base

@click.command()
@click.argument('knowledge_base_file')
def main(knowledge_base_file: str):
    # Load the knowledge base from the specified file
    knowledge_base = load_knowledge_base(knowledge_base_file)
    
    print("Hello! I am your virtual assistant. You can ask me anything.")
    print("Type 'exit' to end the conversation.\n")
    
    # Conversation loop
    while True:
        # Get the user's query
        query = input("You: ")
        
        # Exit if the user types 'exit'
        if query.lower() == 'exit':
            print("Goodbye! Have a nice day!")
            break
        
        # Generate the assistant's response using the language model
        answer = query_model(query, knowledge_base)
        
        # Display the assistant's response
        print(f"Assistant: {answer}\n")
        
        # Extract new knowledge from the conversation
        new_knowledge = extract_knowledge(query, answer)
        
        if new_knowledge:
            # Update the knowledge base
            knowledge_base = update_knowledge_base(knowledge_base, new_knowledge)
            
            # Save the updated knowledge base silently
            with open(knowledge_base_file, 'w') as file:
                file.write(knowledge_base)

if __name__ == "__main__":
    main()
