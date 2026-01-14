"""
Nano Banana MCP Server
Connects to Google's Gemini API for AI image generation.
"""

import os
import base64
import json
import time
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from google import genai
from google.genai import types

# Initialize MCP server
mcp = FastMCP("nanobanana")

# Output directories
OUTPUT_DIR = Path(__file__).parent / "generated_images"
OUTPUT_DIR.mkdir(exist_ok=True)

VIDEO_OUTPUT_DIR = Path(__file__).parent / "generated_videos"
VIDEO_OUTPUT_DIR.mkdir(exist_ok=True)


def get_client():
    """Get configured Gemini client."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    return genai.Client(api_key=api_key)


@mcp.tool()
def generate_image(prompt: str, filename: str = None, aspect_ratio: str = "16:9") -> str:
    """
    Generate an image using Nano Banana (Gemini image generation).

    Args:
        prompt: Detailed description of the image to generate
        filename: Optional filename (without extension). Auto-generated if not provided.
        aspect_ratio: Image aspect ratio - "16:9", "1:1", "9:16", "4:3", "3:4"

    Returns:
        Path to the generated image file
    """
    client = get_client()

    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nanobanana_{timestamp}"

    try:
        # Use Gemini 2.0 Flash for image generation (Nano Banana)
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["image", "text"],
            )
        )

        # Extract and save the image
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                mime_type = part.inline_data.mime_type

                # Determine file extension
                ext = "png" if "png" in mime_type else "jpg"
                filepath = OUTPUT_DIR / f"{filename}.{ext}"

                # Save the image
                with open(filepath, "wb") as f:
                    f.write(image_data)

                return f"Image saved to: {filepath}"

        return "No image was generated. Try a different prompt."

    except Exception as e:
        return f"Error generating image: {str(e)}"


@mcp.tool()
def generate_image_pro(prompt: str, filename: str = None, resolution: str = "1024") -> str:
    """
    Generate a high-quality image using Nano Banana Pro (Gemini 3 Pro Image).
    Better for complex prompts and professional assets.

    Args:
        prompt: Detailed description of the image to generate
        filename: Optional filename (without extension)
        resolution: Image resolution - "1024", "2048", or "4096"

    Returns:
        Path to the generated image file
    """
    client = get_client()

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nanobanana_pro_{timestamp}"

    try:
        # Use Gemini 2.0 Flash experimental for image generation
        # Note: Gemini 3 Pro Image may require different model name when available
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=f"{prompt}\n\nGenerate a high-quality, photorealistic image at {resolution}px resolution.",
            config=types.GenerateContentConfig(
                response_modalities=["image", "text"],
            )
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                mime_type = part.inline_data.mime_type

                ext = "png" if "png" in mime_type else "jpg"
                filepath = OUTPUT_DIR / f"{filename}.{ext}"

                with open(filepath, "wb") as f:
                    f.write(image_data)

                return f"Image saved to: {filepath}"

        return "No image was generated. Try a different prompt."

    except Exception as e:
        return f"Error generating image: {str(e)}"


@mcp.tool()
def edit_image(image_path: str, edit_prompt: str, output_filename: str = None) -> str:
    """
    Edit an existing image using AI.

    Args:
        image_path: Path to the image to edit
        edit_prompt: Description of the edits to make
        output_filename: Optional output filename

    Returns:
        Path to the edited image
    """
    client = get_client()

    if not output_filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"edited_{timestamp}"

    try:
        # Load the image
        image_path = Path(image_path)
        if not image_path.exists():
            return f"Image not found: {image_path}"

        with open(image_path, "rb") as f:
            image_data = f.read()

        # Determine mime type
        ext = image_path.suffix.lower()
        mime_type = "image/png" if ext == ".png" else "image/jpeg"

        # Create the edit request
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[
                types.Part.from_bytes(data=image_data, mime_type=mime_type),
                edit_prompt
            ],
            config=types.GenerateContentConfig(
                response_modalities=["image", "text"],
            )
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                edited_data = part.inline_data.data
                out_mime = part.inline_data.mime_type

                out_ext = "png" if "png" in out_mime else "jpg"
                filepath = OUTPUT_DIR / f"{output_filename}.{out_ext}"

                with open(filepath, "wb") as f:
                    f.write(edited_data)

                return f"Edited image saved to: {filepath}"

        return "No edited image was generated."

    except Exception as e:
        return f"Error editing image: {str(e)}"


@mcp.tool()
def list_generated_images() -> str:
    """
    List all images that have been generated.

    Returns:
        List of generated image files
    """
    images = list(OUTPUT_DIR.glob("*.png")) + list(OUTPUT_DIR.glob("*.jpg"))
    images.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    if not images:
        return "No images generated yet."

    result = "Generated images:\n"
    for img in images[:20]:  # Show last 20
        size_kb = img.stat().st_size / 1024
        result += f"  - {img.name} ({size_kb:.1f} KB)\n"

    return result


@mcp.tool()
def generate_f1_car(
    team: str = "McLaren",
    spec: str = "2024",
    angle: str = "3/4 front",
    background: str = "dark void with reflections"
) -> str:
    """
    Generate an F1 car image with preset styling.

    Args:
        team: Team name (McLaren, Red Bull, Ferrari, Mercedes)
        spec: Year or specification (e.g., "2024", "2024 Miami upgrade")
        angle: Camera angle ("3/4 front", "side profile", "rear 3/4", "front")
        background: Background description

    Returns:
        Path to the generated image
    """
    # Team-specific styling
    team_styles = {
        "McLaren": {
            "car": "MCL38",
            "livery": "papaya orange and blue",
            "details": "distinctive papaya orange color with blue accents"
        },
        "Red Bull": {
            "car": "RB20",
            "livery": "dark blue with red and yellow accents",
            "details": "matte dark blue finish with Red Bull branding"
        },
        "Ferrari": {
            "car": "SF-24",
            "livery": "traditional Ferrari red",
            "details": "iconic Rosso Corsa red with black accents"
        },
        "Mercedes": {
            "car": "W15",
            "livery": "silver and teal",
            "details": "silver base with teal Petronas accents"
        }
    }

    style = team_styles.get(team, team_styles["McLaren"])

    prompt = f"""Subject: A {team} {style['car']} Formula 1 car in {style['livery']} livery, {spec} specification.
{angle} angle view showing the {style['details']}.
The car is centered in a {background}.
Clean, photorealistic render with dramatic studio lighting.
Sharp details on the front wing, halo device, sidepods, and rear wing.
High-quality automotive photography style."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"f1_{team.lower().replace(' ', '_')}_{timestamp}"

    return generate_image(prompt, filename)


@mcp.tool()
def generate_video(
    prompt: str,
    filename: str = None,
    negative_prompt: str = None,
    aspect_ratio: str = "16:9",
    duration_seconds: int = 8
) -> str:
    """
    Generate a video using Veo 3 (Google's video generation AI).

    Args:
        prompt: Detailed description of the video to generate
        filename: Optional filename (without extension)
        negative_prompt: Things to avoid in the video
        aspect_ratio: Video aspect ratio - "16:9", "9:16", "1:1"
        duration_seconds: Video duration (default 8 seconds)

    Returns:
        Path to the generated video file
    """
    client = get_client()

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"veo3_{timestamp}"

    try:
        # Configure video generation
        config_params = {}
        if negative_prompt:
            config_params["negative_prompt"] = negative_prompt
        if aspect_ratio:
            config_params["aspect_ratio"] = aspect_ratio

        config = types.GenerateVideosConfig(**config_params) if config_params else None

        # Start video generation
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt,
            config=config,
        )

        # Wait for completion (video generation takes time)
        max_wait = 300  # 5 minutes max
        waited = 0
        while not operation.done and waited < max_wait:
            time.sleep(10)
            waited += 10
            operation = client.operations.get(operation)

        if not operation.done:
            return "Video generation timed out. Try again or use a simpler prompt."

        # Save the video
        generated_video = operation.result.generated_videos[0]
        filepath = VIDEO_OUTPUT_DIR / f"{filename}.mp4"

        # Download and save
        client.files.download(file=generated_video.video)
        generated_video.video.save(str(filepath))

        return f"Video saved to: {filepath}"

    except Exception as e:
        return f"Error generating video: {str(e)}"


@mcp.tool()
def generate_rotating_video(
    subject: str,
    style: str = "photorealistic",
    background: str = "dark void with reflections",
    filename: str = None
) -> str:
    """
    Generate a smooth 360-degree rotating video of a subject using Veo 3.
    Perfect for product showcases and F1 car presentations.

    Args:
        subject: The subject to rotate (e.g., "McLaren MCL38 F1 car in papaya orange livery")
        style: Visual style - "photorealistic", "cinematic", "studio"
        background: Background description
        filename: Optional filename (without extension)

    Returns:
        Path to the generated video file
    """
    # Build the rotation prompt (based on the example that works)
    prompt = f"""Subject: {subject} centered in a {background}.
Motion Dynamics (Critical): The subject executes a very slow, smooth, and continuous 360-degree spin.
The spinning motion must be completely continuous with constant angular velocity.
Do not pause or freeze during the rotation.
The rotation speed is slow, cinematic, and linear.
Style: {style}, dramatic studio lighting, high-quality render.
Camera: Static camera, subject rotates in place."""

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"rotating_{timestamp}"

    return generate_video(
        prompt=prompt,
        filename=filename,
        negative_prompt="jerky motion, sudden stops, camera movement, blur, distortion"
    )


@mcp.tool()
def generate_f1_rotating_video(
    team: str = "McLaren",
    spec: str = "2024",
    background: str = "dark void with reflections"
) -> str:
    """
    Generate a rotating 360-degree video of an F1 car using Veo 3.
    Perfect for newsletter headers and social media.

    Args:
        team: Team name (McLaren, Red Bull, Ferrari, Mercedes)
        spec: Year or specification (e.g., "2024")
        background: Background description

    Returns:
        Path to the generated video file
    """
    team_styles = {
        "McLaren": {
            "car": "MCL38",
            "livery": "papaya orange and blue",
            "details": "distinctive papaya orange color with blue accents"
        },
        "Red Bull": {
            "car": "RB20",
            "livery": "dark blue with red and yellow accents",
            "details": "matte dark blue finish with Red Bull branding"
        },
        "Ferrari": {
            "car": "SF-24",
            "livery": "traditional Ferrari red",
            "details": "iconic Rosso Corsa red with black accents"
        },
        "Mercedes": {
            "car": "W15",
            "livery": "silver and teal",
            "details": "silver base with teal Petronas accents"
        }
    }

    style = team_styles.get(team, team_styles["McLaren"])
    subject = f"{team} {style['car']} Formula 1 car in {style['livery']} livery, {spec} specification, {style['details']}"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"f1_{team.lower().replace(' ', '_')}_rotating_{timestamp}"

    return generate_rotating_video(
        subject=subject,
        style="photorealistic automotive photography",
        background=background,
        filename=filename
    )


@mcp.tool()
def list_generated_videos() -> str:
    """
    List all videos that have been generated.

    Returns:
        List of generated video files
    """
    videos = list(VIDEO_OUTPUT_DIR.glob("*.mp4"))
    videos.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    if not videos:
        return "No videos generated yet."

    result = "Generated videos:\n"
    for vid in videos[:20]:  # Show last 20
        size_mb = vid.stat().st_size / (1024 * 1024)
        result += f"  - {vid.name} ({size_mb:.1f} MB)\n"

    return result


if __name__ == "__main__":
    mcp.run()
