
def get_first_parameter(name, parameters):
    if name in parameters:
        path = parameters[name][0]
    else:
        return None
    return path

def format_list_to_sui_options(values):
    """
    """
    return [
        dict(name=value, value=value)
        for value in values
    ]

def format_search_results_for_sui(search_results):
    """
        Transform liftree search results to SUI format
    """
    return dict(
        (category, dict(
            name=category,
            results=[
                dict(
                    title=file,
                    url=f'/show?path={file}'
                )
                for file in files
            ]
        ))
        for category, files in search_results.items()
    )
