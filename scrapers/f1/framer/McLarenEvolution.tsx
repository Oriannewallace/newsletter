import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"

/*
 * McLaren MCL38 2024 Evolution Component
 * For use in Framer - shows the car transformation with toggle
 *
 * SETUP:
 * 1. Replace VIDEO_URL with your Veo 3 generated video
 * 2. Or replace IMAGE_URLS with your Nano Banana generated images
 * 3. Import this component into Framer
 */

// Replace these with your actual asset URLs
const ASSETS = {
    video: "YOUR_VEO3_VIDEO_URL_HERE.mp4",
    images: {
        preMiami: "YOUR_NANO_BANANA_IMAGE_1.png",
        miamiUpgrade: "YOUR_NANO_BANANA_IMAGE_2.png",
        finalSpec: "YOUR_NANO_BANANA_IMAGE_3.png",
    }
}

const STAGES = [
    {
        id: "pre-miami",
        label: "Pre-Miami",
        rounds: "Rounds 1-5",
        stats: "19.2 pts/race",
        description: "Traditional sidepod design",
        color: "#FF8000", // McLaren papaya
    },
    {
        id: "miami",
        label: "Miami Upgrade",
        rounds: "Round 6+",
        stats: "+0.5s per lap",
        description: "Hollowed sidepods, new floor",
        color: "#47C7FC", // McLaren blue
    },
    {
        id: "final",
        label: "Championship Spec",
        rounds: "Round 24",
        stats: "31.1 pts/race",
        description: "Refined championship winner",
        color: "#FFD700", // Gold for winner
    },
]

export default function McLarenEvolution() {
    const [activeStage, setActiveStage] = useState(0)
    const [isPlaying, setIsPlaying] = useState(true)
    const [showVideo, setShowVideo] = useState(true)

    const currentStage = STAGES[activeStage]

    return (
        <div style={styles.container}>
            {/* Header */}
            <div style={styles.header}>
                <h2 style={styles.title}>McLaren MCL38 Evolution</h2>
                <p style={styles.subtitle}>How upgrades won the 2024 championship</p>
            </div>

            {/* Main Display */}
            <div style={styles.display}>
                {showVideo ? (
                    <video
                        src={ASSETS.video}
                        autoPlay={isPlaying}
                        loop
                        muted
                        playsInline
                        style={styles.video}
                    />
                ) : (
                    <AnimatePresence mode="wait">
                        <motion.img
                            key={activeStage}
                            src={Object.values(ASSETS.images)[activeStage]}
                            alt={currentStage.label}
                            style={styles.image}
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 1.05 }}
                            transition={{ duration: 0.5 }}
                        />
                    </AnimatePresence>
                )}

                {/* Stats Overlay */}
                <motion.div
                    style={styles.statsOverlay}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    key={activeStage}
                >
                    <span style={styles.statsLabel}>{currentStage.rounds}</span>
                    <span style={{...styles.statsValue, color: currentStage.color}}>
                        {currentStage.stats}
                    </span>
                </motion.div>
            </div>

            {/* Toggle Controls */}
            <div style={styles.controls}>
                {STAGES.map((stage, index) => (
                    <button
                        key={stage.id}
                        onClick={() => setActiveStage(index)}
                        style={{
                            ...styles.stageButton,
                            backgroundColor: activeStage === index ? stage.color : "#1a1a1a",
                            color: activeStage === index ? "#000" : "#fff",
                            borderColor: stage.color,
                        }}
                    >
                        <span style={styles.buttonLabel}>{stage.label}</span>
                        <span style={styles.buttonDesc}>{stage.description}</span>
                    </button>
                ))}
            </div>

            {/* Playback Controls */}
            <div style={styles.playbackControls}>
                <button
                    onClick={() => setShowVideo(!showVideo)}
                    style={styles.iconButton}
                >
                    {showVideo ? "📷 Show Images" : "🎬 Show Video"}
                </button>
                {showVideo && (
                    <button
                        onClick={() => setIsPlaying(!isPlaying)}
                        style={styles.iconButton}
                    >
                        {isPlaying ? "⏸️ Pause" : "▶️ Play"}
                    </button>
                )}
            </div>

            {/* Progress Indicator */}
            <div style={styles.progressBar}>
                {STAGES.map((stage, index) => (
                    <div
                        key={stage.id}
                        style={{
                            ...styles.progressSegment,
                            backgroundColor: index <= activeStage ? stage.color : "#333",
                        }}
                    />
                ))}
            </div>
        </div>
    )
}

const styles: { [key: string]: React.CSSProperties } = {
    container: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "24px",
        backgroundColor: "#0a0a0a",
        borderRadius: "16px",
        fontFamily: "system-ui, -apple-system, sans-serif",
        color: "#fff",
        maxWidth: "800px",
        margin: "0 auto",
    },
    header: {
        textAlign: "center",
        marginBottom: "20px",
    },
    title: {
        fontSize: "28px",
        fontWeight: "700",
        margin: "0 0 8px 0",
        background: "linear-gradient(90deg, #FF8000, #47C7FC)",
        WebkitBackgroundClip: "text",
        WebkitTextFillColor: "transparent",
    },
    subtitle: {
        fontSize: "14px",
        color: "#888",
        margin: 0,
    },
    display: {
        position: "relative",
        width: "100%",
        aspectRatio: "16/9",
        backgroundColor: "#000",
        borderRadius: "12px",
        overflow: "hidden",
        marginBottom: "20px",
    },
    video: {
        width: "100%",
        height: "100%",
        objectFit: "cover",
    },
    image: {
        width: "100%",
        height: "100%",
        objectFit: "cover",
    },
    statsOverlay: {
        position: "absolute",
        bottom: "16px",
        left: "16px",
        display: "flex",
        flexDirection: "column",
        gap: "4px",
        backgroundColor: "rgba(0,0,0,0.7)",
        padding: "12px 16px",
        borderRadius: "8px",
        backdropFilter: "blur(8px)",
    },
    statsLabel: {
        fontSize: "12px",
        color: "#888",
        textTransform: "uppercase",
        letterSpacing: "1px",
    },
    statsValue: {
        fontSize: "24px",
        fontWeight: "700",
    },
    controls: {
        display: "flex",
        gap: "12px",
        width: "100%",
        marginBottom: "16px",
    },
    stageButton: {
        flex: 1,
        padding: "16px 12px",
        border: "2px solid",
        borderRadius: "12px",
        cursor: "pointer",
        transition: "all 0.3s ease",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "4px",
    },
    buttonLabel: {
        fontSize: "14px",
        fontWeight: "600",
    },
    buttonDesc: {
        fontSize: "11px",
        opacity: 0.7,
    },
    playbackControls: {
        display: "flex",
        gap: "12px",
        marginBottom: "16px",
    },
    iconButton: {
        padding: "8px 16px",
        backgroundColor: "#1a1a1a",
        border: "1px solid #333",
        borderRadius: "8px",
        color: "#fff",
        cursor: "pointer",
        fontSize: "13px",
    },
    progressBar: {
        display: "flex",
        width: "100%",
        height: "4px",
        gap: "4px",
        borderRadius: "2px",
        overflow: "hidden",
    },
    progressSegment: {
        flex: 1,
        transition: "background-color 0.3s ease",
    },
}
