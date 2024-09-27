import ollama


def main():
    # Load the summary variable from the file
    with open("content.txt", "r") as file:
        summary = file.read().strip()

    # Add extra text to the summary
    extra_text = "After reading the news earlier, Generate a balanced counter-narrative news story using Llama LLM, presenting at least three alternative perspectives on the news event. Produce three search-worthy headlines reflecting these viewpoints. Utilize sentiment information from sentiment_results.txt for insight.."
    output_text = "give output in the form of a JSON nothing else should be written in your response except this json object. the format of the json object should be {headline1 : " ", sentiment1 : { }, headline2: " " ,sentiment2: { } , headline3 : "", sentiment3: { } }"
    summary_with_extra = f"{summary} {extra_text} {output_text}"

    # Read the contents of sentiment.txt
    with open("sentiment_results.txt", "r") as sentiment_file:
        sentiment_contents = sentiment_file.read()

    # Using Ollama to generate a response
    ollama_response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': f"{summary_with_extra}\n\nOriginal News Sentiments:\n{sentiment_contents}"}])['message']['content']

    # Print the response
    print("Ollama Response:", ollama_response)

    # Save the summary variable to a file
    with open("Results.json", "w") as file:
        file.write(ollama_response)

if __name__ == "__main__":
    main()