from typing import List

from src.predicates.BCondition import BHasCondition
from src.predicates.PredicateTemplate import PredicateTemplate
from src.signal_interpolation.EstimateLikelihood import estimate_likelihood
from src.social_exchange.BSocialExchange import BSocialExchange
from src.types.NPCTypes import BNPCType


def update_beliefs_from_observation(observer: BNPCType, exchange: BSocialExchange, accepted: bool):
    i = exchange.initiator
    r = exchange.responder

    influencing_conditions_i: List[PredicateTemplate] = []
    for rule in exchange.initiator_irs.rules:
        if rule.weight is not None:
            for cond in rule.condition:
                if cond.req_predicate not in influencing_conditions_i:
                    influencing_conditions_i.append(cond.req_predicate)

    for cond in influencing_conditions_i:
        if isinstance(cond, BHasCondition):
            p_template = cond.req_predicate
            pred = p_template.instantiate(subject=i, target=r) if not p_template.is_single else p_template.instantiate(subject=i)

            p_obs_given_true = estimate_likelihood(exchange.initiator_irs, predicate=p_template, pred_true=True, accepted=accepted)
            p_obs_given_false = estimate_likelihood(exchange.initiator_irs, predicate=p_template, pred_true=False, accepted=accepted)

            prior_prob = observer.beliefStore.get_probability(p_template, i, r)
            numerator = p_obs_given_true * prior_prob

            denominator = numerator + p_obs_given_false * (1 - prior_prob)
            if denominator == 0:
                continue
            posterior_prob = numerator / denominator

            observer.beliefStore.update(pred, posterior_prob)

    influencing_conditions_r = []
    for rule in exchange.responder_irs.rules:
        if rule.weight is not None:
            for cond in rule.condition:
                if cond.req_predicate not in influencing_conditions_r:
                    influencing_conditions_r.append(cond.req_predicate)

    for cond in influencing_conditions_r:
        if isinstance(cond, BHasCondition):
            p_template = cond.req_predicate
            pred = p_template.instantiate(subject=r, target=i) if not p_template.is_single else p_template.instantiate(subject=r)

            p_obs_given_true = estimate_likelihood(exchange.responder_irs, predicate=p_template, pred_true=True, accepted=accepted)
            p_obs_given_false = estimate_likelihood(exchange.responder_irs, predicate=p_template, pred_true=False, accepted=accepted)

            prior_prob = observer.beliefStore.get_probability(p_template, r, i)
            numerator = p_obs_given_true * prior_prob

            denominator = numerator + p_obs_given_false * (1 - prior_prob)
            if denominator == 0:
                continue
            posterior_prob = numerator / denominator

            observer.beliefStore.update(pred, posterior_prob)
