import gradio as gr

from src.backend import classify, explain, get_trulens_feedback, predict

# Gradio Theme
theme = gr.themes.Default(
    primary_hue=gr.themes.colors.emerald,
    secondary_hue=gr.themes.colors.green,
)

title = """
<picture>
  <img alt="Logo" src="https://raw.githubusercontent.com/saradiazdelser/SimplifAI/main/static/logo.png" style="width: 14%; margin-bottom: 10px;" />
</picture>

# Let's go and simplif-AI
Our application can be used to simplify texts to make them more accessible
"""

# Gradio UI for the fronted
with gr.Blocks(theme=theme) as demo:
    gr.Markdown(title)

    with gr.Tab("Input"):

        input_textbox = gr.Textbox(
            lines=5, placeholder="Put your complicated text here..."
        )
        submit_butn = gr.Button("Submit")
        output_textbox = gr.Textbox()

        submit_butn.click(fn=predict, inputs=input_textbox, outputs=output_textbox)

        gr.Markdown("### Get a definition for a concept")

        with gr.Row():
            wd_input_textbox = gr.Textbox(
                lines=1, placeholder="Put a concept that you don't understand here..."
            )
            wd_submit_butn = gr.Button("Submit")
        wd_output_textbox = gr.Textbox()

        wd_submit_butn.click(
            fn=explain,
            inputs=[output_textbox, wd_input_textbox],
            outputs=wd_output_textbox,
        )

    with gr.Tab("About the App"):
        gr.Markdown(
            "This App converts any given text into 'plain language', a simplified form of writing designed to enhance understanding for people with diverse cognitive abilities."
        )
        gr.Markdown("## Introduction")
        gr.Markdown(
            "Many individuals with learning or mental disabilities encounter difficulties in comprehending standard English text, limiting their access to information and hindering effective communication. To tackle this issue, we propose a user-friendly web application that effortlessly converts any given English text into 'Plain English,' a simplified form of writing designed to enhance understanding for people with diverse cognitive abilities. By doing so, we aim to ensure that information is not only accessible but also inclusive. The target audience for our web app is broad, encompassing individuals with learning or mental disabilities, caregivers, educators, and anyone aiming to communicate with a diverse audience. By catering to the needs of this demographic, our application fosters inclusivity and ensures that information is comprehensible to a wider spectrum of users. The unique benefit lies in the simplicity of our solution – a tool that makes information universally accessible, bridging the gap and promoting a more inclusive digital environment."
        )
        gr.Markdown("Visit our [GitHub](https://github.com/saradiazdelser/SimplifAI/)")

    with gr.Tab("Trulens Metrics"):

        tl_submit_butn = gr.Button("Get Trulens Metrics")
        tl_output_textbox = gr.TextArea(label="Output:")
        tl_dataframe = gr.Dataframe()

        tl_submit_butn.click(
            fn=get_trulens_feedback, outputs=[tl_dataframe, tl_output_textbox]
        )

    with gr.Tab("Observability"):

        gr.Markdown(
            "Visualization of Attribution for Complexity by token. Generated using TruLen Explainability's implementation of Integrated Gradients."
        )
        input_textbox = gr.Textbox(lines=5, placeholder="Put your text here...")
        submit_butn2 = gr.Button("Submit")
        explain_output = gr.HighlightedText(
            label="SIMPLICITY ATTRIBUTION",
            interactive=True,
            combine_adjacent=True,
            show_legend=True,
        )

        submit_butn2.click(fn=classify, inputs=input_textbox, outputs=explain_output)
