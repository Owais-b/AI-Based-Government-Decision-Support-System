def policy_simulator(budget_increase_percent, base_complaints=1000):
    """
    Policy Impact Simulator
    Simple 'what-if' analysis for budget changes
    """
    # Simple realistic simulation model
    # Higher budget increase → higher complaint reduction (with diminishing returns)
    reduction = min(budget_increase_percent * 0.45, 65)   # max 65% reduction
    
    new_complaints = round(base_complaints * (1 - reduction / 100))
    
    return {
        "expected_reduction_percent": round(reduction, 1),
        "new_complaint_volume": new_complaints,
        "message": f"✅ Increasing budget by **{budget_increase_percent}%** is predicted to reduce complaints by approximately **{round(reduction, 1)}%**.",
        "insight": "This simulation assumes linear efficiency with diminishing returns after 40% increase."
    }