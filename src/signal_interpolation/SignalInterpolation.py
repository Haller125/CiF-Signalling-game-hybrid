from dataclasses import dataclass

from src.predicates.Condition import HasCondition
from src.signal_interpolation.EstimateLikelihood import estimate_likelihood
from src.social_exchange.BSocialExchange import BSocialExchange
from src.types.NPCTypes import BNPCType


def update_beliefs_from_observation(observer: BNPCType, exchange: BSocialExchange, accepted: bool):
    i = exchange.initiator
    r = exchange.responder

    influencing_conditions_i = []
    for rule in exchange.initiator_irs.rules:
        if rule.weight is not None:
            for cond in rule.condition:
                for p_template in cond.req_predicates:
                    if p_template not in influencing_conditions_i:
                        influencing_conditions_i.append(p_template)

    for cond in influencing_conditions_i:
        if isinstance(cond, HasCondition):
            for p_template in cond.req_predicates:
                pred = p_template.instantiate(subject=i, target=r)

                p_obs_given_true = estimate_likelihood(exchange.initiator_irs, predicate=p_template, pred_true=True, accepted=accepted)
                p_obs_given_false = estimate_likelihood(exchange.initiator_irs, predicate=p_template, pred_true=False, accepted=accepted)

                prior_prob = observer.beliefStore.get_probability(pred, i, r)
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
                for p_template in cond.req_predicates:
                    if p_template not in influencing_conditions_r:
                        influencing_conditions_r.append(p_template)

    for cond in influencing_conditions_r:
        if isinstance(cond, HasCondition):
            for p_template in cond.req_predicates:
                pred = p_template.instantiate(subject=r, target=i)

                p_obs_given_true = estimate_likelihood(exchange.responder_irs, predicate=p_template, pred_true=True, accepted=accepted)
                p_obs_given_false = estimate_likelihood(exchange.responder_irs, predicate=p_template, pred_true=False, accepted=accepted)

                prior_prob = observer.beliefStore.get_probability(pred, r, i)
                numerator = p_obs_given_true * prior_prob

                denominator = numerator + p_obs_given_false * (1 - prior_prob)
                if denominator == 0:
                    continue
                posterior_prob = numerator / denominator

                observer.beliefStore.update(pred, posterior_prob)
