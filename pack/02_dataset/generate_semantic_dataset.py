from __future__ import annotations
import json, random
from pathlib import Path

SEED=20260708
random.seed(SEED)
PACK_ROOT=Path(__file__).resolve().parents[1]
ROOT=PACK_ROOT/'outputs/pocket-ai'
DATA=ROOT/'data/semantic_sheet_matching'

SHEET={
 'document_title':'Estrategias_20260527_2119',
 'spreadsheet_id':'1tLNo0_xjtmWKM9Y7PcChFut8S0w0kMKeAvFi9zg52gA',
 'main_sheet':'Data','support_sheet':'Listas','header_row':4,'column_range':'A:AF'
}
COLUMN_MAP={
 'A':'EstrategiaId','B':'ItemMantenible','C':'ModoDeFalla','D':'TipoEstrategia','E':'TareaId','F':'Nombre','G':'TipoTarea','H':'Restriccion',
 'I':'LimitesAceptables','J':'ComentariosCondicionales','K':'Origen','L':'Frecuencia','M':'UnidadTiempo','N':'Especialidad','O':'Labour1','P':'Labour1Cantidad','Q':'Labour1Horas',
 'R':'Labour2','S':'Labour2Cantidad','T':'Labour2Horas','U':'Labour3','V':'Labour3Cantidad','W':'Labour3Horas','X':'Labour4','Y':'Labour4Cantidad','Z':'Labour4Horas',
 'AA':'LabourOtras','AB':'OrigTL1','AC':'OrigTL2','AD':'OrigTL3','AE':'OrigTL4','AF':'Eliminar'
}
REVIEWABLE=['F','I','J','L','M','N','O','P','Q']
PRTS=[
 ('1YD PREV SRVC SCI','SERV EXT SCI',2,16,'SCI','Mantenimiento preventivo anual del sistema contra incendio SCI',['red SCI','panel de incendio','detectores','sirena','bomba jockey','válvula supervisada']),
 ('1MO INS ELEC SEGURIDAD','GACSA SISTEMA POTENCIA SERV EXT',2,2,'POTENCIA','Inspección mensual eléctrica de seguridad en tableros y paneles',['tablero DP','panel LP','puesta a tierra','bloqueo eléctrico','corriente estable','señalización']),
 ('1MO INS SRVC ELEC SALA','GACSA SISTEMA POTENCIA SERV EXT',2,2,'SALA_ELECTRICA','Inspección mensual del servicio eléctrico en sala eléctrica',['sala eléctrica','MCC','celdas','iluminación','ventilación de sala','orden y limpieza']),
 ('1MO MBC PRED TERMOGRAFIA','GACSA SISTEMA POTENCIA SERV EXT',2,4,'TERMOGRAFIA','Termografía mensual predictiva en tableros, borneras y barras',['imagen térmica','punto caliente','barra RST','bornera','interruptor principal','delta térmico']),
 ('1MO MBC PRED ULTRASONIDO','GACSA SISTEMA POTENCIA SERV EXT',2,4,'ULTRASONIDO','Ultrasonido mensual predictivo en componentes eléctricos energizados',['descarga parcial','ruido ultrasónico','corona','tracking','aislador','celda energizada']),
 ('1MO PREV SRVC HVAC','SERV EXT HVAC',3,12,'HVAC','Servicio preventivo mensual HVAC en unidades de climatización',['filtro HVAC','evaporador','condensador','presión de refrigerante','termostato','drenaje']),
 ('1MO PREV SRVC SALA ELEC SCI','SERV EXT SCI',2,6,'SCI_SALA','Preventivo mensual SCI asociado a sala eléctrica',['sala eléctrica SCI','detector de humo','panel de alarma','estación manual','luz estroboscópica','sirena']),
 ('1YD PREV SRVC SALA','GACSA SISTEMA POTENCIA SERV EXT',2,8,'SALA_ELECTRICA','Servicio preventivo anual de sala eléctrica',['sala eléctrica anual','limpieza técnica','tablero general','barras','aislamiento visual','ajuste mecánico']),
 ('1YO MBC SRVC EARTHING SALA','GACSA SISTEMA POTENCIA SERV EXT',2,4,'EARTHING','Servicio anual de medición y verificación de puesta a tierra de sala',['malla a tierra','resistencia de tierra','pozo a tierra','conductor verde amarillo','barra equipotencial','telurómetro']),
 ('2YD PREV SRVC SALA','GACSA SISTEMA POTENCIA SERV EXT',2,8,'SALA_ELECTRICA','Servicio preventivo bienal de sala eléctrica',['preventivo bienal','sala de tableros','celdas MT','limpieza dieléctrica','ajuste de puertas','verificación de barras']),
 ('3MD PREV SRVC HVAC','SERV EXT HVAC',3,36,'HVAC','Servicio preventivo trimestral HVAC de mayor alcance',['mantenimiento trimestral HVAC','serpentín','compresor','ventilador','amperaje HVAC','lavado químico']),
 ('3MO INS SRVC BATTERY BANK','GACSA SISTEMA POTENCIA SERV EXT',2,4,'BATERIAS','Inspección trimestral del banco de baterías',['banco de baterías','voltaje por celda','sulfatación','UPS DC','temperatura de batería','bornes']),
 ('3MO INS SRVC ELEC SALA','GACSA SISTEMA POTENCIA SERV EXT',2,4,'SALA_ELECTRICA','Inspección trimestral del servicio eléctrico de sala',['inspección trimestral','sala eléctrica','alimentadores','tablero de control','estado de interruptores','limpieza visual']),
 ('3MO MBC PRED TERMOGRAFIA','GACSA SISTEMA POTENCIA SERV EXT',2,6,'TERMOGRAFIA','Termografía trimestral predictiva de mayor cobertura',['termografía trimestral','conexión caliente','falso contacto','barra de cobre','breaker','registro termográfico']),
 ('3MO MBC PRED ULTRASONIDO','GACSA SISTEMA POTENCIA SERV EXT',2,6,'ULTRASONIDO','Ultrasonido trimestral predictivo en sala y equipos eléctricos',['ultrasonido trimestral','descarga interna','arco incipiente','ruido eléctrico','aislamiento','registro acústico']),
 ('4YD PREV SRVC BANK CHARGER','GACSA SISTEMA POTENCIA SERV EXT',2,20,'CARGADOR','Servicio preventivo cuatrienal del cargador de baterías',['cargador de baterías','rectificador','flotación DC','ecualización','ripple','alarma charger']),
 ('5YD PREV SRVC RELES','GACSA SISTEMA POTENCIA SERV EXT',2,24,'RELES','Servicio preventivo quinquenal de relés de protección',['relé de protección','inyección secundaria','curva de disparo','pickup','trip','prueba funcional']),
 ('5YD PREV SRVC SALA','GACSA SISTEMA POTENCIA SERV EXT',2,72,'SALA_ELECTRICA','Servicio preventivo quinquenal integral de sala eléctrica',['mantenimiento quinquenal','sala eléctrica integral','celdas completas','torque general','limpieza profunda','prueba dieléctrica']),
 ('6MD PREV SRVC HVAC','SERV EXT HVAC',3,72,'HVAC','Servicio preventivo semestral HVAC integral',['semestral HVAC','recuperación de refrigerante','lavado de serpentines','motor ventilador','presostato','temperatura de impulsión']),
 ('6MD PREV SRVC SALA ELEC SCI','SERV EXT SCI',2,8,'SCI_SALA','Servicio preventivo semestral SCI para sala eléctrica',['semestral SCI','detectores de sala','panel contra incendio','prueba de alarma','lazo supervisado','batería de panel SCI'])
]

def build_record(p,variant,idx):
    code,specialty,people,hh,family,feature,tokens=p
    t0=tokens[variant%len(tokens)]; t1=tokens[(variant+2)%len(tokens)]
    col=REVIEWABLE[(variant+idx)%len(REVIEWABLE)]
    if variant%6==0: col='J'
    elif variant%6==1: col='Q'
    elif variant%6==2: col='N'
    query=f"Reporte de mantenimiento: {t0}; se observó {t1}. Validar similitud con {feature} y proponer actualización controlada para {code}."
    return {
      'query':query,
      'similarity_matching':{'matched_historical_feature':feature,'similarity_score_expected':round(0.82+(variant%11)*0.012,3),'target_row_type':'Fila histórica compatible'},
      'target_analysis':{'predicted_column_letter':col,'predicted_column_name':COLUMN_MAP[col]},
      'tools':[{'type':'function','function':{'name':'match_and_update_sheet','description':'Propone una actualización sin alterar IDs ni estructura.','parameters':{'type':'object','properties':{'prt_code':{'type':'string','default':code},'especialidad_valida':{'type':'string','default':specialty},'horas_hombre_totales':{'type':'integer','default':hh}},'required':['prt_code','especialidad_valida','horas_hombre_totales']}}}],
      'pipeline_routing':{'api_entrypoint':'app.main','router_module':'app.indexer','sheet':SHEET,'column_map':COLUMN_MAP},
      'business_rules_payload':{'prt_code':code,'familia':family,'especialidad_valida':specialty,'labour1_cantidad':people,'labour1_horas_prt_completo':hh,'tarea_id_policy':'No inventar TareaId','estrategia_id_policy':'No inventar EstrategiaId'},
      'metadata_rules':f"PRT {code}; columna {col} ({COLUMN_MAP[col]}); especialidad {specialty}; HH completo {hh}; requiere revisión humana antes de aplicar."
    }

def validate(rows):
    assert len(rows)==360
    assert all(r['target_analysis']['predicted_column_letter'] in REVIEWABLE for r in rows)
    dist={p[0]:0 for p in PRTS}
    for r in rows: dist[r['business_rules_payload']['prt_code']]+=1
    assert set(dist.values())=={18}
    return {'total_records':360,'expected_per_prt':18,'distribution':dist,'status':'VALIDATED_OK'}

def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')

def main():
    rows=[build_record(p,v,i*18+v) for i,p in enumerate(PRTS) for v in range(18)]
    report=validate(rows)
    shuffled=list(rows); random.Random(SEED).shuffle(shuffled); cut=54
    test=shuffled[:cut]; train=shuffled[cut:]
    dump(DATA/'dataset_full.json',rows); dump(DATA/'train_dataset.json',train); dump(DATA/'test_dataset.json',test); dump(DATA/'validation_report.json',report)
    dump(ROOT/'configs/semantic_dataset_config.json',{'project':'pocket-ai','google_sheet_reference':SHEET,'column_map_a_af':COLUMN_MAP,'reviewable_columns':REVIEWABLE,'official_prt_count':len(PRTS)})
    (ROOT/'logs').mkdir(parents=True,exist_ok=True)
    (ROOT/'logs/hailort.log').write_text(f"total_records={len(rows)}\ntrain_records={len(train)}\ntest_records={len(test)}\nstatus=VALIDATED_OK\n",encoding='utf-8')
    print(json.dumps({'status':'OK','full_dataset_records':len(rows),'train_records':len(train),'test_records':len(test),'validation':report['status']},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
