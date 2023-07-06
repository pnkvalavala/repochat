# RepoChat

This project enables users to have interactive conversations about a GitHub repository. By providing the necessary tokens and GitHub link, users can utilize the power of the OpenAI API for computing embeddings, as well as leverage the capabilities of the Deeplake Vector Database by Activeloop. The project currently supports Jurassic-2 LLM by AI21 Labs, but plans to incorporate open-source Hugging Face models like [StarChat-β](https://huggingface.co/HuggingFaceH4/starchat-beta) in the future.

## Usage

To start a conversation about a specific GitHub repository, follow these steps:

1. Open the [RepoChat](https://repochat.streamlit.app/) deployed on Streamlit.
2. Enter all the tokens necessary. Your credentials are only stored in your session state.
3. Enter the GitHub repository link in the provided input field.
4. You can now chat and ask questions about the repository, which will be answered by the integrated LLM model (Jurassic-2).

Please note that the responses may take some time to generate, especially for larger repositories or complex queries. The system will indicate when the model is actively processing a request.

## Future Enhancements

The RepoChat project aims to improve and expand its features in the future. Planned enhancements include:

- Adding support for open-source Hugging Face models like StarChat-β.
- Enhancing the user interface to provide a more intuitive and seamless chatting experience.
- Optimizing the performance and response time of the system for larger repositories.

Stay tuned for updates and new releases!