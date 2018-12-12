
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
