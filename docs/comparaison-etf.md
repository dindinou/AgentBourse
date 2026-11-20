# Comparaison avec les ETF islamiques (20/11/2026)

Les 150 plus grosses actions du MSCI World, passées dans notre calcul, puis comparées à la composition de 4 fonds islamiques : iShares MSCI World Islamic, iShares MSCI USA Islamic, iShares MSCI EM Islamic, SP Funds S&P 500 Sharia.

- Gardées par au moins un fonds islamique : **71** ; écartées par tous : **79**.
- 🚨 **Cas graves** (notre calcul dit conforme, les fonds écartent) : **28**.
  - attrapés par notre détecteur d'activités cachées : **12** : Amazon.Com Inc (AMZN), Meta Platforms Class A (META), Walmart (WMT), Costco Wholesale Corp (COST), Caterpillar Inc (CAT), Netflix (NFLX), Siemens N Ag (SIE.DE), Walt Disney (DIS), Mcdonalds Corp (MCD), Sony Group (6758.T), Recruit Holdings (6098.T), Starbucks Corp (SBUX).
  - ratés par notre détecteur : **16** : Coca-Cola (KO), Roche Ps Par Ag (ROP.SW), Unitedhealth Group (UNH), Novartis Ag (NOVN.SW), Nestle Sa (NESN.SW), Amgen Inc (AMGN), Amphenol Corp Class A (APH), Shopify Subordinate Voting Class A (SHOP.TO), Pfizer (PFE), Unilever Plc (ULVR.L), Eaton Plc (ETN), Advantest (6857.T), Automatic Data Processing Inc (ADP), Parker-Hannifin (PH), Cme Group Class A (CME), Compagnie Financiere Richemont Sa (CFR.SW).
  - Avec la règle « jamais positif sans un fonds islamique », ces cas graves ne reçoivent plus d'avis positif : ils sont affichés « 🟠 Écartée par les fonds islamiques ».
- Fausses alertes (alerte, mais un fonds islamique la garde) : 3 : Alphabet Class A (GOOGL), Alphabet Class C (GOOG), Gilead Sciences (GILD).
- Trop sévères (notre calcul l'écarte, un fonds la garde) : 5 : Welltower (WELL), Salesforce (CRM), Lowes Companies Inc (LOW), Tokyo Electron (8035.T), Marvell Technology (MRVL).
- 🟣 Citées par l'ONU (Gaza, colonies) : **13** : Microsoft (MSFT), Amazon.Com Inc (AMZN), Alphabet Class A (GOOGL), Alphabet Class C (GOOG), Chevron (CVX), Palantir Technologies Class A (PLTR), Caterpillar Inc (CAT), International Business Machines Co (IBM), Allianz (ALV.DE), Blackrock (BLK), Lockheed Martin (LMT), Booking Holdings (BKNG), Bp Plc (BP.L).
  - dont gardées par un fonds islamique (que notre règle bloque en plus) : **7** : Microsoft (MSFT), Alphabet Class A (GOOGL), Alphabet Class C (GOOG), Chevron (CVX), International Business Machines Co (IBM), Booking Holdings (BKNG), Bp Plc (BP.L).

## Détail

| Action | Code | Notre calcul | Alertes | Fonds islamiques qui la gardent | ONU | Résultat final |
|---|---|---|---|---|---|---|
| Apple | AAPL | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Microsoft | MSFT | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | par. 39 à 41 : cloud et IA pour l'armée | citee_onu |
| Nvidia | NVDA | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Amazon.Com Inc | AMZN | majoritaire  | vente en ligne : vend souvent de l'alcool et du porc (activité : Internet Retail) | aucun | par. 41 : cloud et IA (projet Nimbus) | citee_onu |
| Alphabet Class A | GOOGL | majoritaire  | revenus de publicité : exclus par la norme S&P (activité : Internet Content & Information) | SP Funds S&P 500 Sharia | par. 41 : cloud et IA (projet Nimbus) | citee_onu |
| Broadcom Inc | AVGO | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Meta Platforms Class A | META | majoritaire  | revenus de publicité : exclus par la norme S&P (activité : Internet Content & Information) | aucun | — | ecartee |
| Alphabet Class C | GOOG | majoritaire  | revenus de publicité : exclus par la norme S&P (activité : Internet Content & Information) | SP Funds S&P 500 Sharia | par. 41 : cloud et IA (projet Nimbus) | citee_onu |
| Eli Lilly | LLY | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Tesla Inc | TSLA | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Jpmorgan Chase & Co | JPM | non_conforme secteur interdit (Banks - Diversified) | — | aucun | — | non_conforme |
| Berkshire Hathaway Inc Class B | BRK-B | non_conforme secteur interdit (Insurance - Diversified) | — | aucun | — | non_conforme |
| Advanced Micro Devices | AMD | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Micron Technology | MU | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, iShares MSCI EM Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Visa Class A | V | non_conforme secteur interdit (Credit Services) | — | aucun | — | non_conforme |
| Exxonmobil Holdings Corp | XOM | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Johnson & Johnson | JNJ | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Walmart | WMT | majoritaire  | supermarché : vend souvent de l'alcool et du porc (activité : Discount Stores) | aucun | — | ecartee |
| Asml Holding | ASML.AS | majoritaire  | — | iShares MSCI World Islamic | — | majoritaire |
| Mastercard Class A | MA | non_conforme secteur interdit (Credit Services) | — | aucun | — | non_conforme |
| Abbvie | ABBV | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Costco Wholesale Corp | COST | majoritaire  | supermarché : vend souvent de l'alcool et du porc (activité : Discount Stores); alcool (« liquor »); tabac (« tobacco ») | aucun | — | ecartee |
| Procter & Gamble | PG | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Chevron | CVX | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic | par. 58 et 59 : gaz et pétrole | citee_onu |
| Cisco Systems Inc | CSCO | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Coca-Cola | KO | majoritaire  | — | aucun | — | ecartee |
| Home Depot | HD | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Palantir Technologies Class A | PLTR | non_conforme  | — | aucun | par. 42 : IA militaire | non_conforme |
| Roche Ps Par Ag | ROP.SW | majoritaire  | — | aucun | — | ecartee |
| Ge Aerospace | GE | non_conforme secteur interdit (Aerospace & Defense) | — | aucun | — | non_conforme |
| Merck & Co Inc | MRK | majoritaire  | — | iShares MSCI World Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Bank Of America | BAC | non_conforme secteur interdit (Banks - Diversified) | — | aucun | — | non_conforme |
| Unitedhealth Group | UNH | majoritaire  | — | aucun | — | ecartee |
| Palo Alto Networks | PANW | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Philip Morris International | PM | non_conforme tabac | tabac (« tobacco ») | aucun | — | non_conforme |
| Hsbc Holdings Plc | HSBA.L | non_conforme secteur interdit (Banks - Diversified) | — | aucun | — | non_conforme |
| Novartis Ag | NOVN.SW | majoritaire  | — | aucun | — | ecartee |
| Shell | SHEL.L | majoritaire  | — | iShares MSCI World Islamic | — | majoritaire |
| Applied Material Inc | AMAT | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Royal Bank Of Canada | RY.TO | non_conforme secteur interdit (Banks - Diversified) | activité bancaire (« banking services ») | aucun | — | non_conforme |
| Astrazeneca Plc | AZN.L | majoritaire  | — | iShares MSCI World Islamic | — | majoritaire |
| Rtx | RTX | non_conforme secteur interdit (Aerospace & Defense) | — | aucun | — | non_conforme |
| Texas Instrument | TXN | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Thermo Fisher Scientific | TMO | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Nestle Sa | NESN.SW | majoritaire  | — | aucun | — | ecartee |
| Lam Research | LRCX | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Caterpillar Inc | CAT | majoritaire  | filiale de crédit ou d'assurance (« Financial Products segment ») | aucun | par. 45 : bulldozers utilisés à Gaza | citee_onu |
| Goldman Sachs Group | GS | non_conforme secteur interdit (Capital Markets) | activité bancaire (« banking services ») | aucun | — | non_conforme |
| Wells Fargo | WFC | non_conforme secteur interdit (Banks - Diversified) | — | aucun | — | non_conforme |
| Intel Corporation | INTC | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic | — | majoritaire |
| Netflix | NFLX | majoritaire  | divertissement (musique, films) : exclu par les fonds islamiques (activité : Entertainment) | aucun | — | ecartee |
| Crowdstrike Holdings Class A | CRWD | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Linde Plc | LIN | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Amgen Inc | AMGN | majoritaire  | — | aucun | — | ecartee |
| Siemens N Ag | SIE.DE | majoritaire  | filiale de crédit ou d'assurance (« financial services segment ») | aucun | — | ecartee |
| Mitsubishi Ufj Financial Group | 8306.T | non_conforme secteur interdit (Banks - Diversified) | activité bancaire (« Banking Business ») | aucun | — | non_conforme |
| Sap | SAP.DE | majoritaire  | — | iShares MSCI World Islamic | — | majoritaire |
| Walt Disney | DIS | majoritaire  | divertissement (musique, films) : exclu par les fonds islamiques (activité : Entertainment); divertissement (« music distribution ») | aucun | — | ecartee |
| International Business Machines Co | IBM | minoritaire  | — | SP Funds S&P 500 Sharia | par. 38 : base de données biométriques | citee_onu |
| Gilead Sciences | GILD | majoritaire  | tabac (« Tobacco ») | SP Funds S&P 500 Sharia | — | a_verifier |
| Morgan Stanley | MS | non_conforme secteur interdit (Capital Markets) | — | aucun | — | non_conforme |
| Ge Vernova | GEV | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Arista Networks | ANET | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Citigroup | C | non_conforme secteur interdit (Banks - Diversified) | activité bancaire (« banking services ») | aucun | — | non_conforme |
| Toyota Motor | 7203.T | non_conforme  | — | aucun | — | non_conforme |
| Mcdonalds Corp | MCD | majoritaire  | restauration : porc ou alcool possibles (activité : Restaurants) | aucun | — | ecartee |
| Commonwealth Bank Of Australia | CBA.AX | non_conforme secteur interdit (Banks - Diversified) | activité bancaire (« banking services ») | aucun | — | non_conforme |
| Toronto Dominion | TD.TO | non_conforme secteur interdit (Banks - Diversified) | activité d'assurance (« property and casualty insurance »); activité bancaire (« banking services ») | aucun | — | non_conforme |
| Oracle | ORCL | minoritaire  | — | SP Funds S&P 500 Sharia | — | minoritaire |
| Pepsico | PEP | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Allianz | ALV.DE | non_conforme secteur interdit (Insurance - Diversified) | activité bancaire (« banking services ») | aucun | par. 75 et 76 : obligations (via PIMCO) et assurances | non_conforme |
| Verizon Communications Inc | VZ | non_conforme  | — | aucun | — | non_conforme |
| Amphenol Corp Class A | APH | majoritaire  | — | aucun | — | ecartee |
| Analog Devices | ADI | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Kla | KLAC | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Abbott Laboratories | ABT | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Bhp Group Ltd | BHP.AX | majoritaire  | — | iShares MSCI World Islamic | — | majoritaire |
| Nextera Energy | NEE | non_conforme  | — | aucun | — | non_conforme |
| Qualcomm | QCOM | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Totalenergies | TTE.PA | minoritaire  | — | iShares MSCI World Islamic | — | minoritaire |
| Welltower | WELL | non_conforme secteur interdit (REIT - Healthcare Facilities) | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | non_conforme |
| Union Pacific | UNP | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Blackrock | BLK | non_conforme secteur interdit (Asset Management) | — | aucun | par. 75 : investissements | non_conforme |
| Banco Santander | SAN.MC | non_conforme secteur interdit (Banks - Diversified) | activité bancaire (« banking services ») | aucun | — | non_conforme |
| American Express | AXP | non_conforme secteur interdit (Credit Services) | — | aucun | — | non_conforme |
| Conocophillips | COP | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Sony Group | 6758.T | majoritaire  | activité d'assurance (« life insurance ») | aucun | — | ecartee |
| Shopify Subordinate Voting Class A | SHOP.TO | majoritaire  | — | aucun | — | ecartee |
| Pfizer | PFE | minoritaire  | — | aucun | — | ecartee |
| Iberdrola | IBE.MC | non_conforme  | — | aucun | — | non_conforme |
| At&T | T | non_conforme  | — | aucun | — | non_conforme |
| Deere | DE | non_conforme  | filiale de crédit ou d'assurance (« Financial Services segment »); filiale de crédit (« offers wholesale financing ») | aucun | — | non_conforme |
| Charles Schwab | SCHW | non_conforme secteur interdit (Capital Markets) | — | aucun | — | non_conforme |
| Tjx | TJX | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Recruit Holdings | 6098.T | majoritaire  | revenus de publicité : exclus par la norme S&P (activité : Internet Content & Information) | aucun | — | ecartee |
| Salesforce | CRM | insuffisant  | — | SP Funds S&P 500 Sharia | — | insuffisant |
| Ubs Group Ag | UBSG.SW | non_conforme secteur interdit (Banks - Diversified) | — | aucun | — | non_conforme |
| Intuitive Surgical | ISRG | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Rolls-Royce Holdings Plc | RR.L | non_conforme secteur interdit (Aerospace & Defense) | — | aucun | — | non_conforme |
| Schneider Electric | SU.PA | majoritaire  | — | iShares MSCI World Islamic | — | majoritaire |
| Danaher | DHR | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Sumitomo Mitsui Financial Group | 8316.T | non_conforme secteur interdit (Banks - Diversified) | filiale de crédit (« offers loans ») | aucun | — | non_conforme |
| Hitachi | 6501.T | majoritaire  | — | iShares MSCI World Islamic | — | majoritaire |
| Banco Bilbao Vizcaya Argentaria | BBVA.MC | non_conforme secteur interdit (Banks - Diversified) | — | aucun | — | non_conforme |
| S&P Global | SPGI | majoritaire  | — | iShares MSCI World Islamic | — | majoritaire |
| Unilever Plc | ULVR.L | majoritaire  | — | aucun | — | ecartee |
| Progressive | PGR | non_conforme secteur interdit (Insurance - Property & Casualty) | — | aucun | — | non_conforme |
| Accenture Plc Class A | ACN | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Airbus Group | AIR.PA | non_conforme secteur interdit (Aerospace & Defense) | — | aucun | — | non_conforme |
| Vertex Pharmaceuticals | VRTX | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Medtronic Plc | MDT | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Eaton Plc | ETN | majoritaire  | — | aucun | — | ecartee |
| Chubb | CB | non_conforme secteur interdit (Insurance - Property & Casualty) | activité d'assurance (« Life Insurance ») | aucun | — | non_conforme |
| Lair Liquide Societe Anonyme Pour | AI.PA | majoritaire  | — | iShares MSCI World Islamic | — | majoritaire |
| Abb Ltd | ABBN.SW | majoritaire  | — | iShares MSCI World Islamic | — | majoritaire |
| Novo Nordisk Class B | NOVO-B.CO | majoritaire  | — | iShares MSCI World Islamic | — | majoritaire |
| Mckesson Corp | MCK | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Advantest | 6857.T | majoritaire  | — | aucun | — | ecartee |
| Altria Group Inc | MO | non_conforme secteur interdit (Tobacco) | tabac (« tobacco ») | aucun | — | non_conforme |
| Lowes Companies Inc | LOW | non_conforme  | — | SP Funds S&P 500 Sharia | — | non_conforme |
| Tokyo Electron | 8035.T | insuffisant  | — | iShares MSCI World Islamic | — | insuffisant |
| Bristol Myers Squibb | BMY | non_conforme  | — | aucun | — | non_conforme |
| Automatic Data Processing Inc | ADP | majoritaire  | — | aucun | — | ecartee |
| Boeing | BA | non_conforme secteur interdit (Aerospace & Defense) | armement (« weapons ») | aucun | — | non_conforme |
| Unicredit | UCG.MI | non_conforme secteur interdit (Banks - Regional) | activité bancaire (« banking services ») | aucun | — | non_conforme |
| Starbucks Corp | SBUX | majoritaire  | restauration : porc ou alcool possibles (activité : Restaurants) | aucun | — | ecartee |
| Marvell Technology | MRVL | non_conforme  | — | SP Funds S&P 500 Sharia | — | non_conforme |
| Lockheed Martin | LMT | non_conforme secteur interdit (Aerospace & Defense) | armement (« Missiles ») | aucun | par. 32 : avion F-35 | non_conforme |
| Uber Technologies | UBER | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Seagate Technology Holdings Plc | STX | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Safran Sa | SAF.PA | non_conforme secteur interdit (Aerospace & Defense) | — | aucun | — | non_conforme |
| Prologis Reit | PLD | non_conforme secteur interdit (REIT - Industrial) | — | aucun | — | non_conforme |
| British American Tobacco | BATS.L | non_conforme tabac | tabac (« Tobacco ») | aucun | — | non_conforme |
| Booking Holdings | BKNG | majoritaire  | — | SP Funds S&P 500 Sharia | par. 70 et 71 : logements dans les colonies; annexe I, n° 27 (Estados Unidos de América) | citee_onu |
| Parker-Hannifin | PH | majoritaire  | — | aucun | — | ecartee |
| Mizuho Financial Group | 8411.T | non_conforme secteur interdit (Banks - Regional) | — | aucun | — | non_conforme |
| Cme Group Class A | CME | majoritaire  | — | aucun | — | ecartee |
| Bank Of Montreal | BMO.TO | non_conforme secteur interdit (Banks - Diversified) | activité bancaire (« banking services ») | aucun | — | non_conforme |
| Sandisk | SNDK | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Compagnie Financiere Richemont Sa | CFR.SW | majoritaire  | — | aucun | — | ecartee |
| Bp Plc | BP.L | minoritaire  | — | iShares MSCI World Islamic | par. 59 : pétrole et carburant | citee_onu |
| Loreal Sa | OR.PA | majoritaire  | — | iShares MSCI World Islamic | — | majoritaire |
| Marathon Petroleum | MPC | non_conforme  | — | aucun | — | non_conforme |
| Zurich Insurance Group Ag | ZURN.SW | non_conforme secteur interdit (Insurance - Diversified) | — | aucun | — | non_conforme |
| Newmont | NEM | majoritaire  | — | iShares MSCI World Islamic, iShares MSCI USA Islamic, SP Funds S&P 500 Sharia | — | majoritaire |
| Capital One Financial Corp | COF | non_conforme secteur interdit (Credit Services) | — | aucun | — | non_conforme |
| Bank Of Nova Scotia | BNS.TO | non_conforme secteur interdit (Banks - Diversified) | — | aucun | — | non_conforme |
| Stryker | SYK | majoritaire  | — | SP Funds S&P 500 Sharia | — | majoritaire |
| Siemens Energy N Ag | ENR.DE | majoritaire  | — | iShares MSCI World Islamic | — | majoritaire |
| Southern | SO | non_conforme  | — | aucun | — | non_conforme |
