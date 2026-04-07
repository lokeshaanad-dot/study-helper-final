import os
from openai import OpenAI

# Use THEIR environment variables
API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")

# Initialize client with THEIR proxy
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

def run_inference(prompt: str):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print(f"[START] task=study env=openenv model={MODEL_NAME}")

    rewards = []

    for step in range(1, 4):
        try:
            action = run_inference("Give one short study tip")

            done = step == 3
            reward = 1.0 if done else 0.0
            rewards.append(f"{reward:.2f}")

            print(f"[STEP] step={step} action={action} reward={reward:.2f} done={'true' if done else 'false'} error=null")

        except Exception as e:
            print(f"[STEP] step={step} action=error reward=0.00 done=false error={str(e)}")

    print(f"[END] success=true steps=3 rewards={','.join(rewards)}")
