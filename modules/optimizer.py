import pulp


def resource_optimizer(budget, priorities=None):
    """
    Smart Resource Allocation Optimizer
    budget: Total available budget in rupees
    priorities: dict of agency -> weight (default reasonable distribution)
    """
    if priorities is None:
        priorities = {"HPD": 0.45, "DSNY": 0.30, "NYPD": 0.25}
    
    try:
        prob = pulp.LpProblem("Resource_Allocation", pulp.LpMinimize)
        agencies = list(priorities.keys())
        
        # Create variables
        allocation = {a: pulp.LpVariable(f"alloc_{a}", lowBound=0) for a in agencies}
        
        # Dummy objective
        prob += 0
        
        # Budget constraint
        prob += pulp.lpSum(allocation.values()) == budget
        
        # Minimum allocation based on priority
        for a in agencies:
            prob += allocation[a] >= budget * priorities.get(a, 0.2) * 0.7   # at least 70% of ideal share
        
        # Solve
        status = prob.solve(pulp.PULP_CBC_CMD(msg=0))
        
        if status == 1:  # Optimal solution found
            return {a: round(pulp.value(allocation[a]), 2) for a in agencies}
        else:
            # Fallback simple proportional allocation
            total_weight = sum(priorities.values())
            return {a: round(budget * priorities.get(a, 0.2) / total_weight, 2) for a in agencies}
            
    except Exception as e:
        # Fallback if PuLP fails
        total_weight = sum(priorities.values())
        return {a: round(budget * priorities.get(a, 0.2) / total_weight, 2) for a in priorities.keys()}