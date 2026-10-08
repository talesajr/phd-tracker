# Fontes dos dados do mapa (`amazonia.json`)

- **Limite da Amazônia, países e estados**: RAISG — Rede Amazônica de Informação
  Socioambiental Georreferenciada (raisg.org), serviço público
  `geo.socioambiental.org/raisg/rest/services/raisg/rg_srv_mapas_limites/MapServer`
  (camadas 7 "límite utilizado por RAISG", 4 "Internacional" e 5 "Departamental"),
  simplificadas (tolerância 0,02°–0,06°) e com coordenadas arredondadas a 0,01°.
  A propriedade intelectual dos dados é das fontes originais de cada país; ver os
  termos de uso da RAISG. Uso aqui: visualização, com atribuição no mapa.
- **Rios**: Natural Earth, `ne_10m_rivers_lake_centerlines` (domínio público),
  recortados à caixa do limite RAISG, rios com scalerank ≤ 9, simplificados a 0,02°.
- **Cidades** (para estimar acesso e nomear lacunas): Natural Earth,
  `ne_10m_populated_places_simple` (domínio público), recortado à mesma caixa.
- **Leaflet 1.9.4** (`vendor/leaflet/`): cópia de cdnjs conferida pelo hash SRI
  publicado (`SRI.txt`); imagens conferidas contra o pacote npm. Licença BSD-2.
