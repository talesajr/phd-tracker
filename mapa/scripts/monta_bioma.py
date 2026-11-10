"""Monta o limite estrito do bioma Amazônia:
  Brasil  = bioma Amazônia do IBGE (1:250.000)
  fora    = ecorregiões RESOLVE 2017 de floresta úmida amazônica de terras baixas,
            recortadas ao limite biogeográfico RAISG atual e sem o território brasileiro.
uso: monta_bioma.py <ecoregions shp> <amaz_ibge.json> <cerrado_pantanal.json> <atual.json> <saida.geojson>"""
import sys, json
import shapefile
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
from shapely.validation import make_valid
import shapely

# ecorregiões de floresta úmida amazônica (bioma "Tropical & Subtropical Moist Broadleaf")
INCLUIR = {
    505: "Southwest Amazon moist forests", 476: "Madeira-Tapajós moist forests",
    465: "Guianan lowland moist forests", 511: "Uatumã-Trombetas moist forests",
    507: "Tapajós-Xingu moist forests", 473: "Japurá-Solimões-Negro moist forests",
    518: "Xingu-Tocantins-Araguaia moist forests", 483: "Napo moist forests",
    474: "Juruá-Purus moist forests", 466: "Guianan piedmont moist forests",
    484: "Negro-Branco moist forests", 508: "Tocantins/Pindare moist forests",
    446: "Caqueta moist forests", 496: "Purus várzea", 497: "Purus-Madeira moist forests",
    503: "Solimões-Japurá moist forests", 464: "Guianan Highlands moist forests",
    512: "Ucayali moist forests", 469: "Iquitos várzea", 498: "Rio Negro campinarana",
    480: "Marajó várzea", 482: "Monte Alegre várzea", 490: "Pantepui forests & shrublands",
    467: "Gurupa várzea", 463: "Guianan freshwater swamp forests",
}
# fora de propósito (ficam de fora): savanas (Beni, Guianan, Llanos, Cerrado), florestas secas
# (Chiquitano, Mato Grosso, Marañón, Apure-Villavicencio, Bolivian montane), Pantanal, puna e
# páramo, Yungas e demais florestas montanas andinas, mangues e o delta do Orinoco.

eco_shp, amaz_p, cp_p, atual_p, saida = sys.argv[1:6]
r = shapefile.Reader(eco_shp, encoding="latin-1")
partes = []
for i, rec in enumerate(r.iterRecords(fields=["ECO_ID", "ECO_NAME"])):
    if rec["ECO_ID"] in INCLUIR:
        partes.append(make_valid(shape(r.shape(i).__geo_interface__)))
eco = make_valid(unary_union(partes))

amaz = make_valid(unary_union([make_valid(shape(f["geometry"])) for f in json.load(open(amaz_p, encoding="utf-8"))["features"]]))
cp = json.load(open(cp_p, encoding="utf-8"))["features"]
brasil_local = make_valid(unary_union([amaz] + [make_valid(shape(f["geometry"])) for f in cp]))  # Brasil na região
atual = make_valid(shape(json.load(open(atual_p))["features"][0]["geometry"]))

fora = make_valid(eco.intersection(atual.buffer(0.05)).difference(brasil_local))
bioma = make_valid(unary_union([amaz, fora]))
# fecha frestas da costura e remove ilhotas/buracos minúsculos
bioma = make_valid(bioma.buffer(0.01).buffer(-0.01))
def limpar(g, min_area=0.01):
    polys = [g] if g.geom_type == "Polygon" else list(getattr(g, "geoms", []))
    out = []
    for p in polys:
        if p.geom_type != "Polygon" or p.area < min_area:
            continue
        holes = [h for h in p.interiors if shapely.Polygon(h).area >= min_area]
        out.append(shapely.Polygon(p.exterior, holes))
    return shapely.MultiPolygon(out)
bioma = limpar(bioma)
simp = make_valid(bioma.simplify(0.015, preserve_topology=True))
simp = limpar(shapely.set_precision(simp, 0.01))
fc = {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {}, "geometry": mapping(simp)}]}
json.dump(fc, open(saida, "w"), separators=(",", ":"))
n = sum(len(p.exterior.coords) + sum(len(h.coords) for h in p.interiors) for p in simp.geoms)
print(f"polígonos: {len(simp.geoms)} | vértices: {n} | válido: {simp.is_valid} | área ≈ {simp.area:.1f}°²")
