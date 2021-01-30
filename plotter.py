import requests

def plot(function):
	eq=function
	URL = "https://graphsketch.com/render.php?eqn1_color=1&eqn1_eqn="+eq+"&eqn2_color=2&eqn2_eqn=&eqn3_color=3&eqn3_eqn=&eqn4_color=4&eqn4_eqn=&eqn5_color=5&eqn5_eqn=&eqn6_color=6&eqn6_eqn=&x_min=-17&x_max=17&y_min=-10.5&y_max=10.5&x_tick=1&y_tick=1&x_label_freq=5&y_label_freq=5&do_grid=0&do_grid=1&bold_labeled_lines=0&bold_labeled_lines=1&line_width=4&image_w=850&image_h=525"
	file = open("temporaryplot.png", "wb")
	file.write(requests.get(URL).content)
	return file