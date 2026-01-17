import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"

/*
 * McLaren MCL38 2024 Evolution Component
 * For use in Framer - shows the car transformation with toggle
 * Includes hover/tap info card with specs and championship data
 */

// Asset paths - local assets folder. Replace with hosted URLs for production.
const ASSETS = {
    video: "./assets/f1_mclaren_rotating_20260114_104205.mp4",
    images: {
        preMiami: "./assets/mclaren_stage1_pre_miami.png",
        miamiUpgrade: "./assets/mclaren_stage2_miami_upgrade.png",
        finalSpec: "./assets/mclaren_stage3_championship.png",
    }
}

// McLaren MCL38 Technical Specifications
const CAR_SPECS = {
    chassis: "McLaren MCL38",
    engine: "Mercedes-AMG M15 E Performance",
    drivers: ["Lando Norris", "Oscar Piastri"],
    weight: "798 kg (minimum)",
    wheelbase: "3,600 mm",
    suspension: "Push-rod (front), Pull-rod (rear)",
}

// Championship progression data (2024 Constructors)
const CHAMPIONSHIP_JOURNEY = [
    { race: "Bahrain", round: 1, position: 4, points: 28 },
    { race: "Saudi Arabia", round: 2, position: 4, points: 53 },
    { race: "Australia", round: 3, position: 4, points: 79 },
    { race: "Japan", round: 4, position: 4, points: 96 },
    { race: "Miami", round: 6, position: 3, points: 176, highlight: true },
    { race: "Monaco", round: 8, position: 2, points: 258 },
    { race: "Britain", round: 12, position: 2, points: 357 },
    { race: "Hungary", round: 13, position: 1, points: 408, highlight: true },
    { race: "Abu Dhabi", round: 24, position: 1, points: 666, highlight: true },
]

const STAGES = [
    {
        id: "pre-miami",
        label: "Pre-Miami",
        rounds: "Rounds 1-5",
        stats: "19.2 pts/race",
        description: "Traditional sidepod design",
        color: "#FF8000",
        upgradeDetails: "Standard 2024 launch specification",
        position: "4th in standings",
    },
    {
        id: "miami",
        label: "Miami Upgrade",
        rounds: "Round 6+",
        stats: "+0.5s per lap",
        description: "Hollowed sidepods, new floor",
        color: "#47C7FC",
        upgradeDetails: "Revolutionary sidepod undercut, new floor edges, tighter coke-bottle",
        position: "Jumped to 3rd",
    },
    {
        id: "final",
        label: "Championship Spec",
        rounds: "Round 24",
        stats: "31.1 pts/race",
        description: "Refined championship winner",
        color: "#FFD700",
        upgradeDetails: "Optimized aero package, 666 total points",
        position: "Champions!",
    },
]

export default function McLarenEvolution() {
    const [activeStage, setActiveStage] = useState(0)
    const [isPlaying, setIsPlaying] = useState(true)
    const [showVideo, setShowVideo] = useState(false)
    const [showInfoCard, setShowInfoCard] = useState(false)

    const currentStage = STAGES[activeStage]

    return (
        <div style={styles.container}>
            {/* Header */}
            <div style={styles.header}>
                <h2 style={styles.title}>McLaren MCL38 Evolution</h2>
                <p style={styles.subtitle}>How upgrades won the 2024 championship</p>
            </div>

            {/* Main Display - with hover/tap for info card */}
            <div
                style={styles.display}
                onMouseEnter={() => setShowInfoCard(true)}
                onMouseLeave={() => setShowInfoCard(false)}
                onClick={() => setShowInfoCard(!showInfoCard)} // Mobile tap toggle
            >
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

                {/* Stats Overlay (bottom-left) */}
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

                {/* Hover Info Card */}
                <AnimatePresence>
                    {showInfoCard && (
                        <motion.div
                            style={styles.infoCard}
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: 20 }}
                            transition={{ duration: 0.3 }}
                        >
                            {/* Specs Section */}
                            <div style={styles.infoSection}>
                                <h4 style={styles.infoTitle}>Technical Specs</h4>
                                <div style={styles.specGrid}>
                                    <div style={styles.specItem}>
                                        <span style={styles.specLabel}>Power Unit</span>
                                        <span style={styles.specValue}>Mercedes M15</span>
                                    </div>
                                    <div style={styles.specItem}>
                                        <span style={styles.specLabel}>Drivers</span>
                                        <span style={styles.specValue}>NOR / PIA</span>
                                    </div>
                                    <div style={styles.specItem}>
                                        <span style={styles.specLabel}>Weight</span>
                                        <span style={styles.specValue}>798 kg</span>
                                    </div>
                                    <div style={styles.specItem}>
                                        <span style={styles.specLabel}>Suspension</span>
                                        <span style={styles.specValue}>Push/Pull</span>
                                    </div>
                                </div>
                            </div>

                            {/* Upgrade Impact Section */}
                            <div style={styles.infoSection}>
                                <h4 style={styles.infoTitle}>Miami Upgrade Impact</h4>
                                <div style={styles.impactStats}>
                                    <div style={styles.impactItem}>
                                        <span style={styles.impactBefore}>19.2</span>
                                        <span style={styles.impactArrow}>→</span>
                                        <span style={styles.impactAfter}>31.1</span>
                                    </div>
                                    <span style={styles.impactLabel}>pts/race average</span>
                                </div>
                            </div>

                            {/* Championship Journey */}
                            <div style={styles.infoSection}>
                                <h4 style={styles.infoTitle}>Championship Journey</h4>
                                <div style={styles.journeyTrack}>
                                    {[4, 4, 3, 2, 1, 1].map((pos, i) => (
                                        <div
                                            key={i}
                                            style={{
                                                ...styles.journeyDot,
                                                backgroundColor: pos === 1 ? "#FFD700" :
                                                    pos === 2 ? "#47C7FC" :
                                                    pos === 3 ? "#FF8000" : "#666",
                                            }}
                                        >
                                            <span style={styles.journeyPos}>{pos}</span>
                                        </div>
                                    ))}
                                </div>
                                <div style={styles.journeyLabels}>
                                    <span>Bahrain</span>
                                    <span>Abu Dhabi</span>
                                </div>
                            </div>

                            {/* Current Stage Detail */}
                            <div style={{...styles.infoSection, borderBottom: "none"}}>
                                <h4 style={{...styles.infoTitle, color: currentStage.color}}>
                                    {currentStage.label}
                                </h4>
                                <p style={styles.upgradeDetail}>{currentStage.upgradeDetails}</p>
                                <span style={{...styles.positionBadge, backgroundColor: currentStage.color}}>
                                    {currentStage.position}
                                </span>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Hover hint */}
                {!showInfoCard && (
                    <div style={styles.hoverHint}>
                        <span>Hover for specs</span>
                    </div>
                )}
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
                    {showVideo ? "Show Images" : "Show Video"}
                </button>
                {showVideo && (
                    <button
                        onClick={() => setIsPlaying(!isPlaying)}
                        style={styles.iconButton}
                    >
                        {isPlaying ? "Pause" : "Play"}
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
        cursor: "pointer",
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
    // Info Card Styles (glassmorphism)
    infoCard: {
        position: "absolute",
        top: "16px",
        right: "16px",
        width: "280px",
        backgroundColor: "rgba(20, 20, 20, 0.85)",
        backdropFilter: "blur(20px)",
        borderRadius: "16px",
        border: "1px solid rgba(255,255,255,0.1)",
        padding: "16px",
        boxShadow: "0 8px 32px rgba(0,0,0,0.4)",
    },
    infoSection: {
        marginBottom: "12px",
        paddingBottom: "12px",
        borderBottom: "1px solid rgba(255,255,255,0.1)",
    },
    infoTitle: {
        fontSize: "11px",
        fontWeight: "600",
        color: "#888",
        textTransform: "uppercase",
        letterSpacing: "1px",
        margin: "0 0 8px 0",
    },
    specGrid: {
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: "8px",
    },
    specItem: {
        display: "flex",
        flexDirection: "column",
        gap: "2px",
    },
    specLabel: {
        fontSize: "10px",
        color: "#666",
    },
    specValue: {
        fontSize: "13px",
        fontWeight: "600",
        color: "#fff",
    },
    impactStats: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "4px",
    },
    impactItem: {
        display: "flex",
        alignItems: "center",
        gap: "8px",
    },
    impactBefore: {
        fontSize: "20px",
        fontWeight: "700",
        color: "#FF8000",
    },
    impactArrow: {
        fontSize: "16px",
        color: "#47C7FC",
    },
    impactAfter: {
        fontSize: "20px",
        fontWeight: "700",
        color: "#FFD700",
    },
    impactLabel: {
        fontSize: "11px",
        color: "#888",
    },
    journeyTrack: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "8px 0",
        position: "relative",
    },
    journeyDot: {
        width: "28px",
        height: "28px",
        borderRadius: "50%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
        zIndex: 1,
    },
    journeyPos: {
        fontSize: "12px",
        fontWeight: "700",
        color: "#000",
    },
    journeyLabels: {
        display: "flex",
        justifyContent: "space-between",
        fontSize: "10px",
        color: "#666",
    },
    upgradeDetail: {
        fontSize: "12px",
        color: "#aaa",
        margin: "0 0 8px 0",
        lineHeight: 1.4,
    },
    positionBadge: {
        display: "inline-block",
        padding: "4px 12px",
        borderRadius: "12px",
        fontSize: "12px",
        fontWeight: "700",
        color: "#000",
    },
    hoverHint: {
        position: "absolute",
        top: "16px",
        right: "16px",
        backgroundColor: "rgba(0,0,0,0.6)",
        padding: "6px 12px",
        borderRadius: "6px",
        fontSize: "11px",
        color: "#888",
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
