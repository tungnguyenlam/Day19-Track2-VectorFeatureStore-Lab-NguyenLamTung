import sys
from agent import HybridMemoryAgent

def main():
    print("Initializing HybridMemoryAgent... (Loading embedding model)")
    agent = HybridMemoryAgent()

    print("\nSeeding episodic memory...")
    memories = [
        "Tôi đã đọc một bài viết rất hay về Kubernetes architecture và cách scale pods tự động.",
        "Hôm qua tôi tìm hiểu về Cloud Security, đặc biệt là AWS IAM roles và Zero Trust networking.",
        "Scaling infrastructure in production involves using Auto Scaling Groups and Application Load Balancers.",
        "Python 3.12 introduces new features for performance tuning, which is great for ML pipelines."
    ]
    for m in memories:
        agent.remember(m, user_id="u_001")
    print("Memory seeded.")

    queries = [
        # 1. Simple lookup (vector only)
        "What have I read about Kubernetes?",
        
        # 2. Profile-needed
        "Recommend what to read next",
        
        # 3. Fresh-activity
        "What am I focused on lately?",
        
        # 4. Paraphrase (vector wins)
        "Documents about scaling infrastructure?",
        
        # 5. Mixed (hybrid + profile)
        "Give me a cloud security summary"
    ]

    for i, q in enumerate(queries, 1):
        print(f"\n{'='*60}")
        print(f"Demo Query {i}: {q}")
        print(f"{'='*60}")
        context = agent.recall(q, user_id="u_001")
        print(context)

if __name__ == "__main__":
    main()
    sys.exit(0)
