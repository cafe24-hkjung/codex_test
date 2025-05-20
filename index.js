import OpenAI from 'openai';
import dotenv from 'dotenv';
import { config } from 'dotenv';

config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

async function generateCode(prompt) {
  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: "You are a helpful coding assistant. Generate code based on the following description."
        },
        {
          role: "user",
          content: prompt
        }
      ],
      temperature: 0,
      max_tokens: 1000
    });

    return completion.choices[0].message.content;
  } catch (error) {
    console.error('Error:', error);
    return null;
  }
}

// 예제 사용
async function main() {
  const prompt = "Create a function that calculates the fibonacci sequence up to n terms";
  console.log('Prompt:', prompt);
  console.log('\nGenerating code...\n');
  
  const generatedCode = await generateCode(prompt);
  console.log('Generated Code:');
  console.log(generatedCode);
}

main();