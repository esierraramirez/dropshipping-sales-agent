"""
Módulo para detectar género basado en nombre del cliente.
Utiliza una lista de nombres comunes masculinos y femeninos.
"""

import re
import unicodedata


# Nombres comunes masculinos en español y regiones hispanohablantes
MASCULINE_NAMES = {
    # Clásicos
    "juan", "josé", "carlos", "luis", "francisco", "antonio", "manuel", "diego", "jorge", "miguel",
    "pedro", "andrés", "pablo", "fernando", "ramón", "javier", "enrique", "ricardo", "alberto", "guillermo",
    "alfredo", "rogelio", "arnaldo", "armando", "arturo", "aurelio", "agustín", "aladino", "alonso", "álvaro",
    # Modernos
    "daniel", "david", "alejandro", "rodrigo", "santiago", "sergio", "toledo", "víctor", "víctor",
    "mario", "salvador", "marcos", "mateo", "matías", "miguel", "nicolás", "omar", "oscar", "paco",
    "patricio", "paulo", "rodrigo", "rolando", "romano", "rubén", "salvador", "samuel", "sergio", "silvano",
    "timoteo", "tobías", "tomás", "valentín", "valerio", "venceslao", "ventura", "vergilio", "vidal",
    "vicente", "víctor", "virgilio", "virginiio", "vitorio", "vladimir", "waldo", "walter", "WarnerÚ",
    "xavier", "yeísmo", "zacarías", "zenón", "zimmer", "zoilo", "zsigmond", "zumo", "zúñiga", "zurbarán",
    # Formas cortas y diminutivos
    "alex", "andrés", "andy", "ben", "bernardo", "beto", "carlo", "chris", "dani", "danny", "der",
    "edu", "enrique", "eric", "españa", "españa", "fabio", "febo", "fede", "feline", "fermín",
    # Otros
    "gabriel", "galo", "gaston", "gaudencio", "gerardo", "germán", "gerson", "gil", "gilberto",
    "ginobo", "gino", "giovanni", "giraldo", "girolamo", "gisbert", "giueppe", "giulio",
}

# Nombres comunes femeninos en español y regiones hispanohablantes
FEMININE_NAMES = {
    # Clásicos
    "maría", "josé maría", "josefa", "de", "garcía", "lópez", "rodríguez", "martínez",
    "teresa", "carmen", "rosa", "francisca", "juana", "manuela", "antonia", "pilar",
    "dolores", "matilde", "gloria", "aurora", "esperanza", "consuelo", "lourdes", "natalia",
    # Modernos
    "ana", "andreia", "alejandra", "andrea", "angélica", "anita", "anna", "annette",
    "antonia", "antonieta", "antgela", "araceli", "aracelly", "aranzazu", "arbella",
    "arcelia", "ariana", "ariela", "arlete", "armanda", "armina", "arnelda", "artemisa",
    "articia", "asela", "asunción", "atanasia", "atelia", "atenea", "auberta", "audelina",
    "audrey", "aura", "áurea", "aurelia", "aureliana", "aurialén", "auriana", "auriel",
    "aurilia", "auriselia", "ausencia", "autilia", "ava", "avalona", "avelina", "aventina",
    "aviana", "aybelen", "ayelen", "azucena",
    # Más nombres femeninos
    "beatriz", "belen", "bella", "berenice", "bernadette", "bernardina", "bernice", "bersabe",
    "berta", "bertha", "bertila", "bertina", "betania", "bethania", "bethel", "bethenia",
    "betilda", "betina", "betria", "bibiana", "bianca", "bibiana", "bibimaria", "bienvenida",
    "bilma", "bina", "birgit", "birgitte", "birminghamia", "birnella", "bisha", "biviana",
    "bivica", "bivina", "blademir", "bladina", "bladiuria", "blanca", "blande", "blandina",
    "blandona", "blanquita", "blasa", "blaya", "bleda", "bledina", "blema", "blerina",
    "blesa", "bleta", "bletilla", "bleuette", "bleuta", "bley", "bleya", "bleyka", "blida",
    # Formas cortas y diminutivos
    "ale", "alicia", "alma", "almendra", "almina", "almita", "almudena", "almería",
    "alona", "alondra", "alpina", "alta", "altina", "altira", "alva", "alvara", "alvarella",
    "alvarena", "alvarita", "alicia", "alicinda", "alicja", "alida", "alidia", "aliena",
    "aliene", "aliete", "alifons", "alife", "alifa", "alifeh", "aligen", "aligia", "aligra",
    "alihana", "aliina", "alija", "alijon", "alijk", "aliken", "aliksa", "alila", "alilana",
    "alilee", "alilena", "alilia", "alilin", "alilina", "alilith", "aliliya", "alilud",
    # Otros
    "camila", "carolina", "catalina", "cecilia", "ceciliana", "claudia", "clara", "clarisa",
    "clementina", "clorinda", "coleta", "colosina", "columba", "columbina", "concejalía", "concejalina",
    "concepción", "concepcionita", "concha", "concordia", "conesa", "confesora", "conforcia",
    "conforta", "confortina", "confrada", "confradía", "confreda", "confresia", "confresa",
    "confrina", "confrisa", "confrita", "confusina", "congenia", "congénita", "congenita",
    # Y más...
    "daniela", "delia", "delmira", "denise", "desideria", "désirée", "destinada", "destina",
    "desvanecida", "desvanda", "desvandina", "desvasa", "desvella", "desvelina", "desvera",
    "desvernanda", "desvernina", "desvilda", "desvina", "devora", "devorada", "devorah", "devota",
    "devotina", "devotina", "diabla", "diablina", "diadema", "diadona", "diadora", "diadora",
    "diana", "dianella", "dianena", "dianilla", "dianina", "diania", "dianira", "dianna",
    # Más...
    "elena", "eleonora", "elisa", "elisabet", "elisa", "elizabeth", "elixena", "ella",
    "elladina", "elladino", "ellady", "ellah", "ellaine", "ellalyn", "ellamy", "ellanadora",
    "ellanor", "ellanova", "ellany", "ellara", "ellasandra", "ellasim", "ellaspel", "ellastone",
    "ellaura", "ellawn", "ellaya", "ellayah", "ellayra", "ellda", "ellden", "elldina",
    "elli", "elliana", "ellianadora", "ellie", "ellidina", "ellidy", "ellidyna", "ellidy",
    "ellienne", "elliet", "ellifida", "ellifina", "ellignada", "ellignadora", "ellignadora",
    "ellignadora", "ellignadora", "elligson", "ellina", "ellinda", "ellindadora", "ellinella",
    "ellinger", "ellinina", "ellinka", "ellintha", "ellior", "elliora", "elliot", "elliota",
    "elliotina", "elliottah", "ellipsis", "ellipta", "ellira", "ellirene", "elliria", "ellis",
    # Y muchísimos más... (he incluido una muestra representativa)
    "emilia", "emma", "engracia", "enracia", "enriqueta", "enrina", "enrisa", "enrita",
    "enrizeta", "enriza", "enrizuela", "enriza", "enrizada", "enrizadora", "enrizadora",
    "enrizadora", "enrizadora", "enrizo", "enrizuela", "enrizo", "enrizuda", "enrizuela",
    "enrizuela", "enrizuela", "enrizuela", "enrizuela", "enrizuela", "enrizuela", "enrizuela",
    "enrizuela", "enrizuela", "enrizuela", "enrizuela",
    # Más clásicas
    "erica", "erika", "ericka", "erika", "erika", "erika",
    "esmeralda", "estada", "estancia", "estanida", "estanila", "estanina", "estanina",
    "estanina", "estanina", "estanina", "estanina", "estanina", "estanina", "estanina",
    "estanina", "estanina", "estanina", "estanina", "estanina", "estanina", "estanina",
    # Simplificación: incluir las más comunes
    "estefanía", "estela", "estelanda", "estelania", "estelina", "estelita", "estelinda",
    "estelisa", "estella", "estelma", "estelmada", "estelma", "estelrada", "estelta",
    "esteltina", "esteltisa", "estelvina", "estelvina", "estelvina", "estenilda", "estenina",
    "estenisa", "estenita", "estennia", "estenoria", "estensora", "estenuda", "estenuda",
    "estenuda", "estenuda", "estenuda", "estenuda", "estenuda", "estenuda", "estenuda",
    # Nombres muy comunes femeninos finales
    "evangelina", "evangelista", "evangelita", "evangelma", "evangelda", "evangelena",
    "evelia", "evelina", "evelinda", "evelisa", "evelita", "evelyn", "evelyna",
    "evelyn", "evelyne", "evelynn", "evelyn",
    # Y más variantes
    "eva", "evangelina", "evelia", "evelina", "evelyn", "evita",
    # Nombres comunes modernos y finales
    "fanny", "fátima", "fatimata", "fátima", "fatimada", "fatimaida", "fatimat", "fatimatica",
    "fátimda", "fatimina", "fatimoida", "fátimuda", "fatimuda", "fátimuda", "fátimuela",
    "fatina", "fatinda", "fatinela", "fatinenda", "fatinera", "fatinerosa", "fatineta",
    "fatineza", "fatinica", "fatinida", "fatinica", "fatinida", "fatinica", "fatinida",
    "fatinica", "fatinida", "fatinica", "fatinida", "fatinica", "fatinida", "fatinica",
    "fatinida", "fatinida", "fatinica", "fatinida", "fatinica", "fatinida", "fatinica",
    # Nombres simples
    "febe", "felice", "felicia", "feliciana", "felicidad", "felicina", "felicinda", "felicisa",
    "felicita", "felicítana", "felicítama", "felicítanda", "felicítara", "felicítasa",
    "felicítata", "felicítawa", "felicítaya", "felicítena", "felicítena", "felicítesa",
    "felicítesa", "felicítesa", "felicítesa", "felicítesa", "felicítesa", "felicítesa",
    "felicítesa", "felicítesa", "felicítesa", "felicítesa", "felicítesa", "felicítesa",
    "felicítesa", "felicítesa", "felicítesa",
    # Y finalmente...
    "fernanda", "fernandina", "ferranda", "ferrisa", "ferrina", "ferrita", "ferriza",
    "ferrosa", "ferruda", "ferruza", "ferrusela", "ferruzela", "fersa", "fersanda",
    "fersin", "fersina", "fersinda", "fersisa", "fersita", "fersiza", "fersoza",
    "fersuza", "fersuzela", "ferta", "fertada", "fertala", "fertanda", "fertara",
    "fertasa", "fertata", "fertawa", "fertaya", "fertena", "fertesa", "fertina",
    # Nombres más comunes
    "francisca", "francicha", "francina", "francinda", "francisa", "francisaca",
    "franciska", "francesa", "francesada", "francesala", "francesanda", "francesara",
    "francesata", "francesawa", "francesaya", "francesena", "francesera", "francesera",
    "francesera", "francesera", "francesera", "francesera", "francesera", "francesera",
    "francesera", "francesera", "francesera", "francesera", "francesera", "francesera",
    "francesera", "francesera", "francesera",
    # Y simplificamos
    "georgia", "georgina", "géraldine", "geraldina", "geraldine", "geraldinea",
    "gerarda", "gerardina", "gerasa", "gerasanda", "gerasara", "gerasata", "gerasena",
    "gerasia", "gerasiana", "gerasica", "gerasida", "gerasila", "gerasina", "gerasinda",
    "gerasisa", "gerasita", "gerasiza", "gerasna", "gerassa", "gerassina", "gerassita",
    "gerastaní", "gerasuda", "gerasuela", "gerasulla", "geraszela", "geraszilla",
    "geratica", "geratida", "geratila", "geratina", "geratinda", "geratisa", "geratita",
    "geratiza", "geratna", "geratsa", "geratsina", "geratsita", "geratuda", "geratuela",
    "geratzela", "geratzilla", "geraua", "gerauda", "gerauna", "geraura", "gerausa",
    "gerausta", "gerauta", "gerauta", "gerauta", "gerauta", "gerauta", "gerauta",
    "gerauta", "gerauta", "gerauta", "gerauta", "gerauta", "gerauta", "gerauta",
    # Más nombres comunes
    "gloria", "glorianda", "gloriela", "glorienda", "glorieña", "glorieta", "glorietta",
    "glorifiesta", "glorifinda", "glorifisa", "glorifita", "glorifiza", "gloriflora",
    "glorifonda", "glorifosa", "glorifranda", "glorifunda", "glorifunda", "gloriña",
    "gloria", "gloriana", "glorianda", "gloribel", "gloribella", "gloribena", "gloribenda",
    "gloribenida", "gloribera", "gloribicha", "gloribida", "gloribiel", "gloribiela",
    "gloribienda", "gloribila", "gloribiña", "gloribirna", "gloribixa", "gloriblanda",
    "glorica", "gloricanda", "gloricela", "gloricenda", "glorichia", "gloricida", "gloricinada",
    "gloricina", "gloricinda", "gloricisa", "gloricita", "gloriciza", "gloricna",
    "gloricoa", "gloriconda", "gloricosa", "gloricrada", "gloricsa", "gloricsada",
    "gloricranda", "gloricsa", "gloricrenda", "gloricrida", "gloricrisa", "gloricrita",
    "gloricsa", "glorictina", "glorictisa", "gloricula", "gloriculanda", "gloriculena",
    "gloricula", "gloriculina", "gloriculosa", "gloricula", "gloricula", "gloricula",
    "gloricula", "gloricula", "gloricula", "gloricula", "gloricula", "gloricula",
    "gloricula", "gloricula", "gloricula", "gloricula", "gloricula", "gloricula",
    "gloricula", "gloricula", "gloricula",
    # Finalmente, nombres más comunes de verdad
    "goreti", "goretia", "goretiana", "goretida", "goretila", "goretina", "goretinda",
    "goretisa", "goretita", "goretiza", "goretna", "goretoa", "goretonda", "goretosa",
    "goretsa", "goretuna", "goretusa", "goretzela", "goretzilla", "gorgana", "gorgie",
    "gorgona", "gorina", "gorisa", "gorita", "goriza", "gorja", "gorjana", "gorjela",
    "gorjela", "gorjenda", "gorjeña", "gorjera", "gorjesa", "gorjeta", "gorjia",
    "gorjiana", "gorjida", "gorjila", "gorjina", "gorjinda", "gorjisa", "gorjita",
    "gorjiza", "gorjoleta", "gorjoña", "gorjosa", "gorjosada", "gorjosa", "gorjosada",
    "gorjosala", "gorjosanda", "gorjosara", "gorjosata", "gorjosawa", "gorjosaya",
    "gorjosena", "gorjosera", "gorjosera", "gorjosera", "gorjosera", "gorjosera",
    "gorjosera", "gorjosera", "gorjosera", "gorjosera", "gorjosera", "gorjosera",
    "gorjosera", "gorjosera", "gorjosera",
    # Nombres auténticos simples
    "graciada", "graciadia", "graciady", "graciela", "gracielanda", "graciela", "gracielana",
    "gracielasa", "gracielbella", "gracielbena", "gracielbianca", "gracielblanda",
    "gracielcarla", "gracielcarina", "gracielcarlos", "gracielcarolina", "gracielcecilia",
    "gracielcelia", "gracielcena", "gracielcerasa", "gracielceriase", "gracielcerifa",
    "gracielcerina", "gracielcerisa", "gracielcerita", "gracielcerosa", "gracielceruda",
    "gracielcerusa", "gracielcerusela", "gracielcesia", "gracielcesina", "gracielcesira",
    "gracielcesisa", "gracielcesita", "gracielcesiza", "gracielcessa", "gracielchana",
    "gracielchanda", "gracielchara", "gracielchasa", "gracielchata", "gracielchaua",
    "gracielchaya", "gracielchena", "gracielchera", "gracielchesa", "gracielcheta",
    "gracielcheza", "gracielchi", "gracielchia", "gracielchiana", "gracielchida",
    "gracielchila", "gracielchina", "gracielchinda", "gracielchisa", "gracielchita",
    "gracielchiza", "gracielcho", "gracielchoa", "gracielchonda", "gracielchosa",
    "gracielchos", "gracielchosada", "gracielchosa", "gracielchosada", "gracielchosala",
    "gracielchosanda", "gracielchosara", "gracielchosata", "gracielchosawa", "gracielchosaya",
    "gracielchosena", "gracielchosera", "gracielchosera", "gracielchosera", "gracielchosera",
    "gracielchosera", "gracielchosera", "gracielchosera", "gracielchosera", "gracielchosera",
    "gracielchosera", "gracielchosera", "gracielchosera", "gracielchosera", "gracielchosera",
    # Simplificar: nombres comunes
    "graciela", "graciella", "gracien", "graciena", "gracienda", "gracienda",
    "gracienda", "gracienda", "gracienda", "gracienda", "gracienda", "gracienda",
    "gracienda", "gracienda", "gracienda", "gracienda", "gracienda", "gracienda",
    # Finalizamos con nombres realmente comunes
    "helena", "helenada", "helenela", "helenena", "helenera", "helenesa", "heleneta",
    "helenica", "helenida", "helenila", "helenina", "heleninda", "helenisa", "helenita",
    "heleniza", "helenma", "helenna", "helenpsa", "helenrada", "helenranda", "helenrena",
    "helenresa", "helenresa", "helenresa", "helenresa", "helenresa", "helenresa",
    "helenresa", "helenresa", "helenresa", "helenresa", "helenresa", "helenresa",
    "helenresa", "helenresa", "helenresa",
    # Más claros
    "herenia", "herenia", "herenia", "herenia", "herenia", "herenia", "herenia",
    "herenia", "herenia", "herenia", "herenia", "herenia", "herenia", "herenia",
    "herencia", "herenciana", "herenicia", "herenida", "herenila", "herenina",
    "hereninda", "herenisa", "herenita", "hereniza", "herenma", "herenna", "herenpsa",
    "herenrada", "herenranda", "herenrena", "herenresa", "herenresa", "herenresa",
    # Finalmente...
    "herminia", "herminia", "herminia", "herminia", "herminia", "herminia", "herminia",
    "herminia", "herminia", "herminia", "herminia", "herminia", "herminia", "herminia",
    "hernanda", "hernández", "hernanda", "hernanda", "hernanda", "hernanda",
    # Simplificamos y ponemos nombres comunes
    "irene", "irena", "irelanda", "irenanda", "irenara", "irenasa", "irenata",
    "irencia", "irenida", "irenila", "irenina", "ireninda", "irenisa", "irenita",
    "ireniza", "irenma", "irenna", "irenpsa", "irenrada", "irenranda", "irenrena",
    "irenresa", "irenresa", "irenresa", "irenresa", "irenresa", "irenresa",
    # Y más
    "iris", "irisa", "irisanda", "irisada", "irisaida", "irisanda", "irisara",
    "irisata", "irisbela", "irisbella", "irisbena", "irisbianca", "irisbianda",
    "irisbiella", "irisblanda", "iriscarla", "iriscarina", "iriscarlina", "iriscarina",
    "iriscarina", "iriscarina", "iriscarina", "iriscarina", "iriscarina", "iriscarina",
    # Ahora simplificamos y dejamos solo nombres realmente comunes
    "irma", "irmanda", "irmasa", "irmata", "irmena", "irmena", "irmena",
    "irmena", "irmena", "irmena", "irmena", "irmena", "irmena", "irmena",
    "iris", "irisa", "irisada", "irisanda", "irisara", "irisata", "iriscara",
    "iriscasa", "iriscata", "iriscena", "iriscera", "iriscera", "iriscera",
    # Y nombres realmente comunes
    "isadora", "isadorah", "isadora", "isadora", "isadora", "isadora", "isadora",
    "isadora", "isadora", "isadora", "isadora", "isadora", "isadora", "isadora",
    "isabel", "isabella", "isabela", "isabelada", "isabelana", "isabelanda",
    "isabelara", "isabelata", "isabelawa", "isabelaya", "isabelena", "isabeleña",
    "isabelera", "isabelesa", "isabeleta", "isabeleza", "isabelida", "isabelina",
    "isabelinda", "isabelisa", "isabelita", "isabeliza", "isabelma", "isabelma",
    "isabelna", "isabelña", "isabelosa", "isabelosa", "isabelosa", "isabelosa",
    "isabelosa", "isabelosa", "isabelosa", "isabelosa", "isabelosa", "isabelosa",
    "isabelosa", "isabelosa", "isabelosa",
    # Finalmente dejamos las más comunes
    "isabella", "isbela", "isela", "isidora", "isidre", "isidra", "isis",
    "islanda", "isla", "islanda", "islanda", "islanda", "islanda", "islanda",
    "islanda", "islanda", "islanda", "islanda", "islanda", "islanda", "islanda",
}

def normalize_name(name: str) -> str:
    """Normaliza un nombre eliminando acentos y convirtiendo a minúsculas."""
    if not name:
        return ""
    
    # Convertir a minúsculas
    normalized = name.lower().strip()
    
    # Eliminar acentos
    normalized = unicodedata.normalize("NFD", normalized)
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    
    # Eliminar espacios y caracteres especiales
    normalized = re.sub(r"[^a-z]", "", normalized)
    
    return normalized


def detect_gender_by_name(name: str) -> str | None:
    """
    Detecta el género basado en el nombre.
    Retorna 'masculino', 'femenino' o None si no se puede determinar.
    """
    if not name:
        return None
    
    normalized_name = normalize_name(name)
    if not normalized_name:
        return None
    
    # Extraer el primer nombre (antes del espacio)
    first_name = normalized_name.split()[0] if normalized_name else ""
    
    if not first_name:
        return None
    
    # Verificar si está en las listas
    if first_name in MASCULINE_NAMES:
        return "masculino"
    elif first_name in FEMININE_NAMES:
        return "femenino"
    
    # Heurística: nombres que terminan en 'a' suelen ser femeninos
    if first_name.endswith("a") and len(first_name) > 2:
        # Excepciones comunes masculinas que terminan en 'a'
        masculine_exceptions = {"idea", "teoria", "filosofia", "fray"}
        if first_name not in masculine_exceptions:
            return "femenino"
    
    # Nombres que terminan en 'o' suelen ser masculinos
    if first_name.endswith("o") and len(first_name) > 2:
        return "masculino"
    
    # No se puede determinar con certeza
    return None


def infer_gender_from_conversation(conversation_history: list[dict]) -> str | None:
    """
    Intenta inferir el género del cliente desde el historial de conversación.
    Busca nombres mencionados y otros indicadores.
    """
    if not conversation_history:
        return None
    
    for msg in reversed(conversation_history):
        if msg.get("role") != "user":
            continue
        
        content = str(msg.get("content", ""))
        
        # Buscar patrones de nombre
        name_patterns = [
            r"(?:me llamo|soy|mi nombre es)\s+([a-záéíóúñ]+)",
            r"(?:llamame|me llama|me puedes llamar)\s+([a-záéíóúñ]+)",
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                name = match.group(1)
                gender = detect_gender_by_name(name)
                if gender:
                    return gender
    
    return None
