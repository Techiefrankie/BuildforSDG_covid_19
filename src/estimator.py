def estimator(data):
    """
      covid_19 estimations
      :param data:
      :return output:
      """
    # challenge 1:
    # currently infected people
    impact_currently_infected = data.get("reportedCases") * 10
    impactsevere_currently_infected = data.get("reportedCases") * 50

    # number of infected people at a requested time
    # get the timeToElapse property and get its factor of 3, since currently infected value doubles in 3 days
    period = data.get("timeToElapse")
    projection = 2 ** period // 3  # get the nearest whole number
    # get the effective projection values for impact and severe
    impact_inf_req_time = impact_currently_infected * projection
    impactsevere_inf_req_time = impactsevere_currently_infected * projection

    # challenge 2:
    # estimated number of severe positive cases that will require hospitalization to recover.
    impact_sev_cases_req_time = 0.15 * impact_inf_req_time
    impactsevere_sev_cases_req_time = 0.15 * impactsevere_inf_req_time

    # number of available beds assuming 35% of hospital beds available for covid_19 cases
    beds_available = data.get("totalHospitalBeds") * 0.35
    impact_hospital_bed = beds_available - impact_sev_cases_req_time
    impactsevere_hospital_bed = beds_available - impactsevere_sev_cases_req_time

    # challenge 3:
    # cases that would require ICU
    impact_cases_icu_req_time = 0.05 * impact_inf_req_time
    impactsevere_cases_icu_req_time = 0.05 * impactsevere_inf_req_time

    # cases that would require ventilator
    impact_cases_vent_req_time = 0.02 * impact_inf_req_time
    impactsevere_cases_vent_req_time = 0.02 * impactsevere_inf_req_time

    # estimated loss of money in the economy
    avg_daily_income_pop = data.get("region").get("avgDailyIncomePopulation")
    avg_daily_income_usd = data.get("region").get("avgDailyIncomeInUSD")

    impact_dollars_in_flight = (impact_inf_req_time * avg_daily_income_pop) * avg_daily_income_usd * period
    impactsevere_dollars_in_flight = (impactsevere_inf_req_time * avg_daily_income_pop) * avg_daily_income_usd * period

    output = {
        "data": data,
        "impact": {
            "currentlyInfected": impact_currently_infected,
            "infectionsByRequestedTime": impact_inf_req_time,
            "severeCasesByRequestedTime": impact_sev_cases_req_time,
            "hospitalBedsByRequestedTime": impact_hospital_bed,
            "casesForICUByRequestedTime": impact_cases_icu_req_time,
            "casesForVentilatorsByRequestedTime": impact_cases_vent_req_time,
            "dollarsInFlight": impact_dollars_in_flight
        },
        "severeImpact": {
            "currentlyInfected": impactsevere_currently_infected,
            "infectionsByRequestedTime": impactsevere_inf_req_time,
            "severeCasesByRequestedTime": impactsevere_sev_cases_req_time,
            "hospitalBedsByRequestedTime": impactsevere_hospital_bed,
            "casesForICUByRequestedTime": impactsevere_cases_icu_req_time,
            "casesForVentilatorsByRequestedTime": impactsevere_cases_vent_req_time,
            "dollarsInFlight": impactsevere_dollars_in_flight
        }
    }

    return output
