# Fontes dos dados do mapa (`amazonia.json`)

- **Limite do bioma Amazônia** (estrito: sem Cerrado, Pantanal, savanas e florestas secas):
  - **Brasil**: bioma Amazônia do IBGE, Biomas 1:250.000 (camada `CREN:lm_bioma_250` do
    GeoServer do IBGE).
  - **Fora do Brasil**: ecorregiões RESOLVE Ecoregions 2017 (Dinerstein et al. 2017, *BioScience*)
    de floresta úmida amazônica de terras baixas, várzeas, campinaranas, florestas das Guianas e
    Pantepui, recortadas ao limite biogeográfico da RAISG. Excluídas: savanas (Beni, Guianas,
    Llanos, Cerrado), florestas secas (Chiquitano, Marañón), Pantanal, puna/páramo, Yungas e
    demais florestas montanas andinas, mangues e delta do Orinoco.
  - Lista exata das ecorregiões e o script: `mapa/scripts/monta_bioma.py` (requer shapely e pyshp).
  - Simplificado a ~1,5 km e arredondado a 0,01°: serve para visualização e para a grade de
    cobertura; para figuras de artigo, refaça a partir das fontes originais.
- **Países e estados**: RAISG (raisg.org), serviço público
  `geo.socioambiental.org/raisg/rest/services/raisg/rg_srv_mapas_limites/MapServer`
  (camadas 4 "Internacional" e 5 "Departamental"), simplificadas.
- **Rios**: Natural Earth, `ne_10m_rivers_lake_centerlines` (domínio público),
  recortados à caixa do limite RAISG, rios com scalerank ≤ 9, simplificados a 0,02°.
- **Cidades** (para estimar acesso e nomear lacunas): Natural Earth,
  `ne_10m_populated_places_simple` (domínio público), recortado à mesma caixa.
- **Leaflet 1.9.4** (`vendor/leaflet/`): cópia de cdnjs conferida pelo hash SRI
  publicado (`SRI.txt`); imagens conferidas contra o pacote npm. Licença BSD-2.
