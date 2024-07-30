import gradio as gr
import json
from datetime import timedelta

def format_time(seconds):
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = round(td.microseconds / 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def json_to_srt(json_text):
    try:
        data = json.loads(json_text)
        srt_lines = []
        for i, item in enumerate(data, 1):
            start_time = format_time(item['start'])
            end_time = format_time(item['end'])
            srt_lines.append(f"{i}\n{start_time} --> {end_time}\n{item['text']}\n")
        return "\n".join(srt_lines)
    except json.JSONDecodeError:
        return "錯誤: 無效的JSON格式"
    except KeyError as e:
        return f"錯誤: JSON中缺少必要的鍵 {str(e)}"

def clear_input():
    return ""

def create_srt_file(srt_text):
    with open("output.srt", "w", encoding="utf-8") as f:
        f.write(srt_text)
    return "output.srt"

with gr.Blocks() as app:
    gr.Markdown("# JSON to SRT Converter")
    
    with gr.Row():
        with gr.Column():
            json_input = gr.Textbox(label="JSON Input", lines=10, placeholder="在這裡貼上JSON...")
            convert_btn = gr.Button("轉換")
            clear_btn = gr.Button("清空輸入")
        
        with gr.Column():
            srt_output = gr.Textbox(label="SRT Output", lines=10, interactive=False)
            download_btn = gr.Button("下載SRT文件")
            file_output = gr.File(label="下載的文件")

    clear_btn.click(clear_input, outputs=[json_input])
    convert_btn.click(json_to_srt, inputs=[json_input], outputs=[srt_output])
    download_btn.click(create_srt_file, inputs=[srt_output], outputs=[file_output])

if __name__ == "__main__":
    app.launch(server_name='0.0.0.0', show_api=False, share=False)