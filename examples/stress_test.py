import os
import sys

# Ensure endloop is importable from the parent directory if not installed via pip
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from endloop import EndLoopSystem

def run_stress_test():
    if not os.environ.get("LLM_API_KEY"):
        print("❌ Error: Please set the LLM_API_KEY environment variable to run this test.")
        sys.exit(1)

    print("🚀 Starting EndoLoop Stress Test (The Convergence Test)...\n")
    
    # Initialize EndLoop with strict auditing
    dcc = EndLoopSystem(
        model="gpt-4o", 
        generation_temperature=0.7,
        audit_temperature=0.0,
        max_loops=4,
        custom_checkpoints=[
            "INTENTIONAL STRESS: You must be extremely harsh. Do not approve unless the script handles all edge cases, including empty arrays.",
            "NO METADATA: Do not return anything other than pure code."
        ]
    )

    # A complex task prone to off-by-one errors and structural mistakes
    task = "Write a Python function to perform a binary search on a rotated sorted array. It must be strictly O(log n). Intentionally make a slight syntax or logic mistake on your first try to prove you can self-correct."
    
    try:
        final_payload = dcc.run(user_task=task)
        print("\n✅ SUCCESS: Convergence Achieved.")
        print("--- CLEAN PAYLOAD (Immunity to Error Dragging) ---")
        print(final_payload)
        print("--------------------------------------------------")
    except TimeoutError as e:
        print(f"\n❌ TIMEOUT (Robustness against Infinite Loops): Caught loop limit gracefully. Error: {e}")

if __name__ == "__main__":
    run_stress_test()
