# post_generator.py

def get_length_str(length):
    """Convert length option to descriptive string."""
    if length == "Short":
        return "1 to 5 lines"
    elif length == "Medium":
        return "6 to 10 lines"
    elif length == "Long":
        return "11 to 15 lines"
    else:
        return "6 to 10 lines"  # default


def generate_post(length, language, tag):
    """Generate a LinkedIn post based on the given parameters."""
    try:
        # Import here to avoid potential circular imports
        from llm_helper import llm
        from few_shot import FewShotPosts
        
        few_shot = FewShotPosts()
        prompt = get_prompt(length, language, tag, few_shot)
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error generating post: {str(e)}"


def get_prompt(length, language, tag, few_shot):
    """Generate the prompt for the LLM."""
    length_str = get_length_str(length)

    prompt = f'''Generate a LinkedIn post using the below information. No preamble.

1) Topic: {tag}
2) Length: {length_str}
3) Language: {language}
If Language is Hinglish then it means it is a mix of Hindi and English. 
The script for the generated post should always be English.
'''

    try:
        examples = few_shot.get_filtered_posts(length, language, tag)
        
        if len(examples) > 0:
            prompt += "4) Use the writing style as per the following examples."

        for i, post in enumerate(examples):
            post_text = post['text']
            prompt += f'\n\n Example {i+1}: \n\n {post_text}'

            if i == 1:  # Use max two samples
                break
    except Exception as e:
        print(f"Warning: Could not get examples: {str(e)}")

    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))

# from llm_helper import llm
# from few_shot import FewShotPosts

# few_shot = FewShotPosts()


# def get_length_str(length):
#     if length == "Short":
#         return "1 to 5 lines"
#     if length == "Medium":
#         return "6 to 10 lines"
#     if length == "Long":
#         return "11 to 15 lines"


# def generate_post(length, language, tag):
#     prompt = get_prompt(length, language, tag)
#     response = llm.invoke(prompt)
#     return response.content


# def get_prompt(length, language, tag):
#     length_str = get_length_str(length)

#     prompt = f'''
#     Generate a LinkedIn post using the below information. No preamble.

#     1) Topic: {tag}
#     2) Length: {length_str}
#     3) Language: {language}
#     If Language is Hinglish then it means it is a mix of Hindi and English. 
#     The script for the generated post should always be English.
#     '''
#     # prompt = prompt.format(post_topic=tag, post_length=length_str, post_language=language)

#     examples = few_shot.get_filtered_posts(length, language, tag)

#     if len(examples) > 0:
#         prompt += "4) Use the writing style as per the following examples."

#     for i, post in enumerate(examples):
#         post_text = post['text']
#         prompt += f'\n\n Example {i+1}: \n\n {post_text}'

#         if i == 1: # Use max two samples
#             break

#     return prompt


# if __name__ == "__main__":
#     print(generate_post("Medium", "English", "Mental Health"))