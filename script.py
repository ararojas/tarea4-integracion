import requests
from xml.etree import ElementTree
import gspread

credentials = {}


def obtener_datos(node_fact):
    country = node_fact.findtext("COUNTRY")
    sex = node_fact.findtext("SEX")
    year = node_fact.findtext("YEAR")
    ghe_causes = node_fact.findtext("GHECAUSES")
    age_group = node_fact.findtext("AGEGROUP")
    display = node_fact.findtext("Display")
    numeric = node_fact.findtext("Numeric")
    low = node_fact.findtext("Low")
    high = node_fact.findtext("High")
    return [country, sex, year, ghe_causes, age_group, display, numeric, low, high]


def importar_pais(pais: str, sheet, row):
    response = requests.get(
        f"http://tarea-4.2021-1.tallerdeintegracion.cl/gho_{pais}.xml")
    tree = ElementTree.fromstring(response.content)
    row_inicial = row
    indicators = ["Number of infant deaths",
                  "Number of deaths",
                  "Number of under-five deaths",
                  "Mortality rate for 5-14 year-olds (probability of dying per 1000 children aged 5-14 years)",
                  "Adult mortality rate (probability of dying between 15 and 60 years per 1000 population)",
                  "Estimates of number of homicides",
                  "Crude suicide rates (per 100 000 population)",
                  "Mortality rate attributed to unintentional poisoning (per 100 000 population)",
                  "Number of deaths attributed to non-communicable diseases, by type of disease and sex",
                  "Estimated road traffic death rate (per 100 000 population)",
                  "Estimated number of road traffic deaths",
                  "Prevalence of underweight among adults, BMI < 18.5 (age-standardized estimate) (%)",
                  "Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol)",
                  "Estimate of daily cigarette smoking prevalence (%)",
                  "Estimate of daily tobacco smoking prevalence (%)",
                  "Estimate of current cigarette smoking prevalence (%)",
                  "Estimate of current tobacco smoking prevalence (%)",
                  "Mean systolic blood pressure (crude estimate)",
                  "Mean fasting blood glucose (mmol/l) (crude estimate)",
                  "Mean Total Cholesterol (crude estimate)"
                  ]
    substrings = ["Mean BMI",
                  "Prevalence of obesity among",
                  "Prevalence of overweight among",
                  "Prevalence of underweight among",
                  "Prevalence of thinness among children and adolescents"]

    datos = []
    for node_fact in tree:
        gho = node_fact.find("GHO").text
        if gho in indicators or any([substring in gho for substring in substrings]):
            row += 1
            fila = [gho]
            fila = fila + obtener_datos(node_fact)
            datos.append(fila)

    sheet.update(f'A{row_inicial + 1}:J{row}', datos)
    return row


gc = gspread.service_account_from_dict(credentials)

sh = gc.open("Tarea4-TI")
headers = [["Indicator (GHO)", "Country", "Sex", "Year", "GHE Causes", "Age Group", "Display", "Numeric",
            "Low", "High"]]
sheet1 = sh.sheet1
sheet1.update(f'A1:J1', headers)
row = 1
row = importar_pais("CHL", sheet1, row)
row = importar_pais("DEU", sheet1, row)
row = importar_pais("USA", sheet1, row)
row = importar_pais("NZL", sheet1, row)
row = importar_pais("ZAF", sheet1, row)
importar_pais("CHN", sheet1, row)
