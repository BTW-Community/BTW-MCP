from btw_mcp import *

vanilla_jars()
btw_jars()
decompile()
setup_new_git_repo()
btw_splashes()
patch()
import_release("import")
package_release("tags/decomp_fix", "tags/import", directory="rel2")