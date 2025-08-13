#region IMPORTS
from classes.ui.pages import Pages
from classes.ui.textelement import TextElement
#endregion

#region PAGE CONFIGURATION
Pages(name="Dashboard", icon="📊", page_layout="wide")
#endregion

#region PAGE'S HEADER
TextElement.set_title("📊 Dashboard")
TextElement.write_text("---")
#endregion