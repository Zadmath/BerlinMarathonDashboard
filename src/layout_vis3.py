import plotly.graph_objects as go

def configure_layout(fig, nations_sorted, years, times_text, runner_statistics, runner_photo_url, selected_category, selected_genre):
    fig.update_layout(
        annotations=[
            dict(
                text=times_text,
                xref="paper", yref="paper",
                x=0.480, y=1.15,  # Position above the title
                showarrow=False,
                align="center",
                bgcolor="white",
                bordercolor="black",
                font=dict(size=12, color="black")
            ),
            dict(
                text=runner_statistics,
                xref="paper", yref="paper",
                x=1, y=1,
                showarrow=False,
                bgcolor="white",
                bordercolor="black",
                borderwidth=1,
                borderpad=4,
                align="left",
                font=dict(size=12)
            )
        ]
    )

    # fleche pour Eliud Kipchoge
    if selected_genre == "ALL" and selected_category == "ALL":
        if "Kenya" in nations_sorted:
            kipchoge_x = 2023 + 0.35
            kipchoge_y = nations_sorted.index("Kenya")
            fig.add_annotation(
                x=kipchoge_x,
                y=kipchoge_y,
                ax=kipchoge_x + 0.7,
                ay=kipchoge_y + 0.5,
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                text="Eliud Kipchoge<br>Recordman 2023",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="black",
                font=dict(size=12, color="black"),
                bgcolor="white",
                bordercolor="black",
                borderwidth=1
            )
    if selected_genre == "W" and selected_category == "ALL":
        if "Ethiopia" in nations_sorted:
            fig.add_annotation(
                x=2023 + 0.35,
                y=nations_sorted.index("Ethiopia"),
                ax=2023 + 1.05,
                ay=nations_sorted.index("Ethiopia") + 0.5,
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                text="Assefa Tigst<br>Recordwoman 2023",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="black",
                font=dict(size=12, color="black"),
                bgcolor="white",
                bordercolor="black",
                borderwidth=1
            )
    # Add a clickable Google Image search link
    if runner_photo_url:
        fig.add_annotation(
            dict(
                xref="paper", yref="paper",
                x=1, y=0.85,
                align="left",
                showarrow=False,
                text=f'<a href="{runner_photo_url}" target="_blank">Voir les images du coureur</a>',
                font=dict(size=13, color="blue"),
                bgcolor="rgba(255, 255, 255, 1)",
                bordercolor="rgba(0, 0, 0, 1)"
            )
        )

    return fig
