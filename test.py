from viz.split_rect import SplitRect


r = SplitRect(
    choices=[0, 1, 2, 3, 0], corrects=[0, 1, 0, 1, 0],
    colors=["#ff0000", "#00ff00", "#0000ff", "#ffff00"]
)
r.save_gif("temp.gif")
