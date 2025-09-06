# Language Learning Platform Requirements

## Business Requirements

- Develop a language learning platform centered on a core vocabulary database of 2,000 words.
- Target students and general users who want to improve their language skills, focusing on vocabulary and sentence construction.
- Provide engaging, AI-driven study activities including writing practice, immersive games, visual novel reading, sentence construction, and flashcards.
- Ensure learning is accessible primarily to users with good internet connectivity in urban areas.
- Use generative AI models with a strategy prioritizing cloud-first deployment and evaluation of OpenAI, Anthropic Claude (via AWS Bedrock), and open-source alternatives like DeepSeek.

## Functional Requirements

- Implement a cloud-first AWS technology strategy focused on scalability and reliability.
- Prioritize integration of Anthropic Claude via AWS Bedrock with thorough performance and integration testing.
- Evaluate OpenAI models for performance before full commitment.
- Use open-source models such as DeepSeek as a flexible, cost-effective backup alternative.
- Ensure AI-generated content delivery for vocabulary practice and sentence construction.
- Support gamification features to increase user engagement.
- Provide personalized learning experiences via AI-driven content.
- Deliver multi-platform access (web and mobile) for users.
- Maintain traceability and monitoring of AI content generation workflow.
- Users access the language portal to select word groups and initiate study sessions.
- Manage study activities including:
  - Writing Practising App
  - Text Adventure Immersion Game
  - Light Visual Novel Immersion Reading
  - Sentence Constructor (using RAG, vector DB, prompt cache, LLM 7B with guardrails)
  - Visual Flashcard Vocabulary

## Non-Functional Requirements

- Performance: Ensure low latency responses to maintain smooth user experience.
- Scalability: Support multiple users in concurrent sessions seamlessly.
- Security: Enforce input/output guardrails to maintain content safety.
- Privacy: Protect user data and interactions securely within cloud infrastructure.
- Flexibility: Architect system for easy model swaps, prompt updates, and dataset expansions.
- Future Proofing: Adopt a modular cloud-first architecture allowing integration of newer AI models and technologies.
