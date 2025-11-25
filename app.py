from io import BytesIO
from PIL import Image
import streamlit as st

def convert(dst):
    # RGBA または LA モードの場合は RGB に変換
    if dst.mode in ("RGBA", "LA", "P"):
        rgb_dst = Image.new("RGB", dst.size, (255, 255, 255))
        if dst.mode == "P":
            dst = dst.convert("RGBA")
        rgb_dst.paste(dst, mask=dst.split()[-1] if dst.mode in ("RGBA", "LA") else None)
        dst = rgb_dst
    elif dst.mode != "RGB":
        dst = dst.convert("RGB")
    return dst

def main():
    st.markdown("# DROP EXIF")
    img_file_buffer = st.file_uploader("ファイルを指定")
    if img_file_buffer is not None:
        with Image.open(img_file_buffer) as src:
            # 画像を表示
            st.image(src, caption=f"{img_file_buffer.name}", use_column_width=True)
            
            data = src.getdata()
            mode = src.mode
            size = src.size
            if "parameters" in src.info:
                parameters = src.info["parameters"]
                st.code(parameters, language="")
                                
                with Image.new(mode, size) as dst:
                    dst.putdata(data)
                    dst = convert(dst)
                    buf = BytesIO()
                    dst.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    st.download_button(
                        label="Download image",
                        data=byte_im,
                        file_name=f"nometa_{img_file_buffer.name}",
                        mime="image/png"
                    )
            else:
                st.text("no exif")
                with Image.new(mode, size) as dst:
                    dst.putdata(data)
                    dst = convert(dst)
                    buf = BytesIO()
                    dst.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    st.download_button(
                        label="Download image",
                        data=byte_im,
                        file_name=f"nometa_{img_file_buffer.name}",
                        mime="image/png"
                    )

if __name__ == "__main__":
    main()
