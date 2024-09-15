from transformers import pipeline

# Initialize the text generation pipeline with GPT-2 (or another model)
generator = pipeline('text-generation', model='gpt2')  # Replace 'gpt2' with a larger model if available

def generate_battlecard(competitor_data, own_product_info):
    try:
        # Build the competitor data string
        competitors_str = '\n'.join([f"Name: {comp['name']}, Strengths: {comp.get('strengths')}, Weaknesses: {comp.get('weaknesses')}" 
                                     for comp in competitor_data])

        # Create a structured prompt
        prompt = (
            f"Generate a detailed battlecard comparing these competitors with our product:\n\n"
            f"Competitors Data:\n{competitors_str}\n\n"
            f"Our Product: {own_product_info}\n\n"
            f"Include key points, comparisons, and actionable recommendations."
        )

        # Generate text using the Hugging Face pipeline
        result = generator(prompt, max_length=500, num_return_sequences=1, do_sample=True, temperature=0.7)

        # Return the generated text
        return result[0]['generated_text'].strip()

    except Exception as e:
        # Log the error for debugging
        print(f"Error generating battlecard: {e}")
        return "Error generating battlecard. Please try again later."
