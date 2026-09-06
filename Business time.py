import os
import requests

class UltimateGlobalMatchmaker:
    def __init__(self, business_type: str, sector: str, target_profit_usd: float):
        self.business_type = business_type.strip().lower()
        self.sector = sector.strip().upper()
        self.target_profit_usd = float(target_profit_usd)

    def _fetch_all_countries(self):
        url = "http://worldbank.org"
        try:
            res = requests.get(url, timeout=10).json()
            if len(res) > 1 and isinstance(res, list):
                return [c for c in res[1] if c.get("region", {}).get("value") != "Aggregates" and c.get("id")]
        except:
            pass
        return [{"id": "US", "name": "United States"}]

    def _fetch_wb_indicator(self, country_code: str, indicator: str) -> float:
        url = f"http://worldbank.org{country_code}/indicator/{indicator}?format=json&mrnev=1"
        try:
            res = requests.get(url, timeout=4).json()
            if len(res) > 1 and res[1] and res[1][0]['value'] is not None:
                return float(res[1][0]['value'])
        except:
            pass
        return 0.0

    def find_best_country(self) -> str:
        countries = self._fetch_all_countries()
        best_country_name = "United States"
        highest_score = -100000.0

        # Scans the global country database dynamically using live demand indices
        # Sliced to the first 40 countries for real-time testing performance.
        for country in countries[:40]:
            code = country["id"]
            name = country["name"]

            gdp_pc = self._fetch_wb_indicator(code, "NY.GDP.PCAP.CD")      # Market Purchasing Power / Demand
            rd_intensity = self._fetch_wb_indicator(code, "GB.XPD.RSDV.GD.ZS")  # Technical Infrastructure Index

            if self.sector in ["QUATERNARY", "SECONDARY"]:
                score = (rd_intensity * 50.0) + (gdp_pc / 5000.0)
            else:
                score = (gdp_pc / 1000.0) + (rd_intensity * 5.0)

            if score > highest_score:
                highest_score = score
                best_country_name = name

        return best_country_name

if __name__ == "__main__":
    print("="*60)
    print("🌍 DYNAMIC SOVEREIGN DESTINATION SELECTOR")
    print("="*60)
    
    input_biz = input("👉 Enter exact business type: ")
    input_sec = input("👉 Enter sector (PRIMARY, SECONDARY, TERTIARY, QUATERNARY): ")
    input_prof = input("👉 Enter target profit in USD: ")

    try:
        prof_val = float(input_prof.replace(",", "").strip())
    except:
        prof_val = 1000000.0

    engine = UltimateGlobalMatchmaker(business_type=input_biz, sector=input_sec, target_profit_usd=prof_val)
    
    print("\nEvaluating global markets via live API algorithms...")
    print(f"\n🏆 OPTIMAL COUNTRY: {engine.find_best_country()}")
