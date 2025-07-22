from src.irs.BIRS import BInfluenceRuleSet
from src.irs.IRS import InfluenceRuleSet
from src.predicates.Predicate import Predicate
from src.predicates.PredicateTemplate import PredicateTemplate
from src.social_exchange.SocialExchange import SocialExchange

def estimate_likelihood(irs: BInfluenceRuleSet, predicate: PredicateTemplate, pred_true: bool, accepted: bool) -> float:
    relevant_rules = []

    for rule in irs.rules:
        for condition in rule.condition:
            for p_template in condition.req_predicates:
                if predicate is p_template:
                    # assuming that the rule's weight is a float value between 0 and 1
                    relevant_rules.append(rule)
                    break

    if not relevant_rules:
        return 0.5

    avg_weight = sum(rule.weight for rule in relevant_rules) / len(relevant_rules)

    if pred_true:
        if accepted:
            return avg_weight
        else:
            return 1 - avg_weight
    else:
        if accepted:
            return 1 - avg_weight
        else:
            return avg_weight

