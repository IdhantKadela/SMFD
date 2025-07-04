import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display

def euler_maruyama_paths(S0, T, n_steps, drift, diffusion, n_paths):
    # Simulating the euler-maruyama processes
    dt = T / n_steps

    S = np.zeros((n_paths, n_steps + 1))
    S[:, 0] = S0

    for i in range(1, n_steps + 1):
        dW = np.random.normal(0, np.sqrt(dt), n_paths)
        S[:, i] = S[:, i - 1] + drift * S[:, i - 1] * dt + diffusion * S[:, i - 1] * dW

    return S # (n_paths, n_steps + 1)

def evaluate_option_euler(option_type, S, K, T, rf):
    ST = S[:,-1]
    ST_arith = np.mean(S, axis=1)
    ST_geom = np.exp(np.mean(np.log(S), axis = 1))
    ST_min = np.min(S, axis = 1)

    # Calculating payoff of each option type
    if option_type == "euro_call":
        P = np.maximum(ST - K, 0).mean()

    elif option_type == "arith_asian_call":
        P = np.maximum(ST_arith - K, 0).mean()

    elif option_type == "geom_asian_call":
        P = np.maximum(ST_geom - K, 0).mean()

    elif option_type == "float_lback_call":
        P = np.maximum(ST - ST_min, 0).mean()

    else:
        raise ValueError("option_type must be one of: 'euro_call', 'arith_asian_call', 'geom_asian_call', 'float_lback_call'")

    return np.exp(-rf * T) * P, P


# Widget to select Option type
message = widgets.HTML("<h1>Interactive Window</h1>")
option_type = widgets.Dropdown(
    options=[('European Call', 'euro_call'),
             ('Arithmetic Asian Call', 'arith_asian_call'),
             ('Geometric Asian Call', 'geom_asian_call'),
             ('Floating Lookback Call', 'float_lback_call')],
    value='euro_call',
    description='Option Type'
)

# variable to save simulation
simulation = None

def interactive_window():
    # Sliders for simulation and pricing params
    S0 = widgets.FloatSlider(value=100, min=1, max=500, step=1, description='Current Spot')
    drift = widgets.FloatSlider(value=0.2, min=-1.0, max=1.0, step=0.05, description='Drift')
    diffusion = widgets.FloatSlider(value=0.2, min=0.01, max=1.0, step=0.01, description='Diffusion')
    T = widgets.FloatSlider(value=1.0, min=0.01, max=5.0, step=0.01, description='Time (years)')
    n_steps = widgets.IntSlider(value=1000, min=100, max=10000, step=100, description='# Steps')
    n_paths = widgets.IntSlider(value=1000, min=0, max=10000, step=100, description='# Paths')
    K = widgets.FloatSlider(value=120, min=1, max=500, step=1, description='Strike')
    rf = widgets.FloatSlider(value=0.05, min=0.0, max=0.5, step=0.01, description='Risk-free Rate')


    # buttons to trigger simulation and pricing
    run_button = widgets.Button(description="Run Simulation")
    price_button = widgets.Button(description="Price Option")

    # Simulation running indicator
    running_label = widgets.HTML(value="")  # Empty by default

    # output widget to display results
    run_output = widgets.Output()
    price_output = widgets.Output()
    price_output.append_stdout(f"Option Type     |Price  |S0     |K      |r    \n")

    # Callback function for the run button click event
    def on_run_button_clicked(b):
        running_label.value = "<span style='color:blue; font-weight:bold;'>Simulation running...</span>"
        run_output.clear_output() # Clear previous output

        with run_output:
            # run simulation and save it
            global simulation
            simulation = euler_maruyama_paths(S0.value, T.value, n_steps.value, 
                                              drift.value, diffusion.value, n_paths.value)
            # plot the simulation
            plt.figure(figsize=(10, 6))
            colors = ['red', 'green', 'navy']
            for i in range(n_paths.value):
                plt.plot(np.linspace(0, T.value, n_steps.value + 1), simulation[i], lw=0.8, alpha=0.5, color=colors[i%3])
            plt.title(f'Simulated {n_paths.value} Paths (drift = {drift.value:.3f}, diffusion = {diffusion.value:.3f})')
            plt.xlabel('Time')
            plt.ylabel('Stock Price')
            plt.grid()
            plt.show()

        # set the label to completed
        running_label.value = "<span style='color:green; font-weight:bold;'>Simulation Completed</span>"


    # Callback function for the price button click event
    def on_price_button_clicked(b):
        # price_output.clear_output() # Clear previous output

        with price_output:
            try:
                # use the saved simulation
                global simulation
                # offseted simulation used to avoid re-simulating when only S0 is varied
                simulation_ = simulation + S0.value - simulation[0,0]
                price, payoff = evaluate_option_euler(option_type.value, simulation_, K.value, T.value, rf.value)
                print(f"{option_type.value:<16}|{price:<7.2f}|{S0.value:<7.2f}|{K.value:<7.2f}|{rf.value:.2f}")
            except(TypeError):
                display(widgets.HTML("<span style='color:red; font-weight:bold;'>Run Simulation First</span>"))


    # attach the callback function to the run_button and price_button
    run_button.on_click(on_run_button_clicked)
    price_button.on_click(on_price_button_clicked)

    # arrange widgets in a layout
    run_box = widgets.VBox([S0, T, drift, diffusion, n_steps, n_paths, run_button, running_label])
    price_box = widgets.VBox([option_type, S0, K, rf, price_button])
    ui = widgets.VBox([run_box, price_box, price_output, run_output])
    ui = widgets.VBox([message, ui])

    # display the ui
    display(ui)