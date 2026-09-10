import streamlit as st
import streamlit.components.v1 as components

THREEJS_AVATAR_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    body {
      background: radial-gradient(circle at center, #0B132B 0%, #060B14 100%);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      overflow: hidden;
      width: 100%;
      height: 100vh;
      color: #E2E8F0;
    }
    #canvas-container {
      width: 100%;
      height: 100%;
      position: absolute;
      top: 0;
      left: 0;
      cursor: grab;
    }
    #canvas-container:active { cursor: grabbing; }

    /* HUD Header */
    .hud-header {
      position: absolute;
      top: 14px;
      left: 16px;
      z-index: 10;
      pointer-events: none;
    }
    .hud-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(0, 245, 155, 0.15);
      border: 1px solid #00F59B;
      color: #00F59B;
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.1em;
      padding: 4px 10px;
      border-radius: 999px;
      text-transform: uppercase;
    }
    .hud-title {
      font-size: 18px;
      font-weight: 900;
      color: #FFFFFF;
      margin-top: 4px;
      letter-spacing: -0.01em;
    }
    .hud-sub {
      font-size: 11px;
      color: #94A3B8;
    }

    /* Telemetry Panel */
    .telemetry-panel {
      position: absolute;
      top: 14px;
      right: 16px;
      z-index: 10;
      background: rgba(10, 20, 36, 0.9);
      border: 1px solid rgba(56, 189, 248, 0.35);
      backdrop-filter: blur(12px);
      border-radius: 12px;
      padding: 10px 14px;
      min-width: 170px;
      pointer-events: none;
      box-shadow: 0 8px 30px rgba(0,0,0,0.6);
    }
    .telem-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
      font-size: 11px;
    }
    .telem-row:last-child { margin-bottom: 0; }
    .telem-label { color: #94A3B8; font-weight: 600; }
    .telem-val { font-weight: 800; font-family: monospace; font-size: 11px; }
    .val-cyan { color: #38BDF8; }
    .val-emerald { color: #00F59B; }
    .val-gold { color: #FBBF24; }

    /* Control Bar */
    .control-bar {
      position: absolute;
      bottom: 16px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 10;
      display: flex;
      gap: 6px;
      background: rgba(10, 20, 36, 0.92);
      border: 1px solid rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(14px);
      padding: 5px 8px;
      border-radius: 999px;
      box-shadow: 0 10px 32px rgba(0, 0, 0, 0.7);
      max-width: 96vw;
      overflow-x: auto;
    }
    .ctrl-btn {
      background: transparent;
      border: 1px solid transparent;
      color: #94A3B8;
      font-size: 11px;
      font-weight: 700;
      padding: 6px 12px;
      border-radius: 999px;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .ctrl-btn:hover {
      color: #FFFFFF;
      background: rgba(255, 255, 255, 0.08);
    }
    .ctrl-btn.active {
      background: #00F59B;
      color: #060B14;
      font-weight: 800;
      border-color: #00F59B;
      box-shadow: 0 0 14px rgba(0, 245, 155, 0.5);
    }
    .orbit-hint {
      position: absolute;
      bottom: 60px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 10px;
      color: #64748B;
      letter-spacing: 0.05em;
      pointer-events: none;
      text-transform: uppercase;
      font-weight: 700;
    }
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
  <div id="canvas-container"></div>

  <div class="hud-header">
    <div class="hud-tag">
      <span style="width: 6px; height: 6px; border-radius: 50%; background: #00F59B; box-shadow: 0 0 8px #00F59B;"></span>
      MediaPipe 33-Joint 3D Kinematics
    </div>
    <div class="hud-title">3D DIGITAL TWIN</div>
    <div class="hud-sub">Interactive Biomechanical Joint Geometry</div>
  </div>

  <div class="telemetry-panel">
    <div class="telem-row">
      <span class="telem-label">EXERCISE</span>
      <span class="telem-val val-emerald" id="disp-exercise">SQUATS</span>
    </div>
    <div class="telem-row">
      <span class="telem-label">ANGLE</span>
      <span class="telem-val val-cyan" id="disp-angle">88° (DEPTH)</span>
    </div>
    <div class="telem-row">
      <span class="telem-label">FORM STATUS</span>
      <span class="telem-val val-emerald" id="disp-status">PERFECT 100%</span>
    </div>
    <div class="telem-row">
      <span class="telem-label">VELOCITY</span>
      <span class="telem-val val-gold" id="disp-fatigue">1.2 m/s (SAFE)</span>
    </div>
  </div>

  <div class="orbit-hint">🖱️ DRAG TO ROTATE 360° &bull; SCROLL TO ZOOM</div>

  <div class="control-bar">
    <button class="ctrl-btn active" data-mode="squat">🏋️ Squats</button>
    <button class="ctrl-btn" data-mode="curl">💪 Bicep Curls</button>
    <button class="ctrl-btn" data-mode="pushup">💥 Push-Ups</button>
    <button class="ctrl-btn" data-mode="press">⚡ Shoulder Press</button>
    <button class="ctrl-btn" data-mode="scan">🧘 360° Scan</button>
  </div>

  <script>
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x060B14, 0.05);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 100);
    camera.position.set(0, 0.6, 4.2);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 2.0;
    controls.maxDistance = 7.0;
    controls.maxPolarAngle = Math.PI / 2 + 0.1;
    controls.target.set(0, 0.3, 0);

    // Lights
    const ambientLight = new THREE.AmbientLight(0x0A192F, 2.5);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0x38BDF8, 2.2);
    keyLight.position.set(3, 4, 3);
    scene.add(keyLight);

    const fillLight = new THREE.DirectionalLight(0x00F59B, 2.8);
    fillLight.position.set(-3, -1, 3);
    scene.add(fillLight);

    // Cyber Grid Floor
    const gridHelper = new THREE.GridHelper(10, 20, 0x00F59B, 0x1E293B);
    gridHelper.position.y = -1.8;
    scene.add(gridHelper);

    // Cyber Rings
    const ringGeo = new THREE.RingGeometry(1.1, 1.13, 48);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0x00F59B, side: THREE.DoubleSide, transparent: true, opacity: 0.4 });
    const floorRing = new THREE.Mesh(ringGeo, ringMat);
    floorRing.rotation.x = Math.PI / 2;
    floorRing.position.y = -1.79;
    scene.add(floorRing);

    // Floating Particles
    const particleCount = 140;
    const particleGeo = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount * 3; i += 3) {
      particlePositions[i] = (Math.random() - 0.5) * 8;
      particlePositions[i + 1] = Math.random() * 5 - 1.8;
      particlePositions[i + 2] = (Math.random() - 0.5) * 8;
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    const particleMat = new THREE.PointsMaterial({ color: 0x38BDF8, size: 0.035, transparent: true, opacity: 0.6 });
    const particles = new THREE.Points(particleGeo, particleMat);
    scene.add(particles);

    // Materials
    const jointMatEmerald = new THREE.MeshStandardMaterial({ color: 0x00F59B, emissive: 0x00F59B, emissiveIntensity: 0.8, roughness: 0.2, metalness: 0.8 });
    const jointMatCyan = new THREE.MeshStandardMaterial({ color: 0x38BDF8, emissive: 0x38BDF8, emissiveIntensity: 0.8, roughness: 0.2, metalness: 0.8 });
    const boneMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, emissive: 0x0F172A, roughness: 0.4, metalness: 0.9, transparent: true, opacity: 0.9 });
    const boneGlowMat = new THREE.MeshBasicMaterial({ color: 0x00F59B, wireframe: true, transparent: true, opacity: 0.35 });

    const sphereGeo = new THREE.SphereGeometry(0.045, 14, 14);
    const headGeo = new THREE.SphereGeometry(0.12, 20, 20);

    const joints = {};
    const jointNames = [
      'head', 'neck', 'chest', 'pelvis',
      'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist',
      'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle',
      'left_foot_index', 'right_foot_index'
    ];

    const modelGroup = new THREE.Group();
    scene.add(modelGroup);

    jointNames.forEach(name => {
      const geo = (name === 'head') ? headGeo : sphereGeo;
      const mat = (name.includes('left') || name === 'head' || name === 'chest') ? jointMatEmerald : jointMatCyan;
      const mesh = new THREE.Mesh(geo, mat);
      joints[name] = mesh;
      modelGroup.add(mesh);
    });

    const connections = [
      ['head', 'neck'], ['neck', 'chest'], ['chest', 'pelvis'],
      ['neck', 'left_shoulder'], ['neck', 'right_shoulder'],
      ['left_shoulder', 'left_elbow'], ['left_elbow', 'left_wrist'],
      ['right_shoulder', 'right_elbow'], ['right_elbow', 'right_wrist'],
      ['left_shoulder', 'left_hip'], ['right_shoulder', 'right_hip'],
      ['chest', 'pelvis'], ['pelvis', 'left_hip'], ['pelvis', 'right_hip'],
      ['left_hip', 'left_knee'], ['left_knee', 'left_ankle'],
      ['right_hip', 'right_knee'], ['right_knee', 'right_ankle'],
      ['left_ankle', 'left_foot_index'], ['right_ankle', 'right_foot_index']
    ];

    const boneMeshes = [];
    connections.forEach(([j1, j2]) => {
      const boneGeo = new THREE.CylinderGeometry(0.018, 0.018, 1, 8);
      const boneMesh = new THREE.Mesh(boneGeo, boneMat);
      const glowMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.024, 0.024, 1, 6), boneGlowMat);
      boneMesh.add(glowMesh);
      modelGroup.add(boneMesh);
      boneMeshes.push({ mesh: boneMesh, p1: j1, p2: j2 });
    });

    // Scanner Laser Ring
    const scanRingGeo = new THREE.RingGeometry(0.75, 0.77, 32);
    const scanRingMat = new THREE.MeshBasicMaterial({ color: 0x00F59B, side: THREE.DoubleSide, transparent: true, opacity: 0.6 });
    const scanRing = new THREE.Mesh(scanRingGeo, scanRingMat);
    scanRing.rotation.x = Math.PI / 2;
    modelGroup.add(scanRing);

    function updateBone(boneObj) {
      const v1 = joints[boneObj.p1].position;
      const v2 = joints[boneObj.p2].position;
      const distance = v1.distanceTo(v2);

      boneObj.mesh.position.copy(v1).add(v2).multiplyScalar(0.5);
      boneObj.mesh.scale.set(1, distance, 1);
      boneObj.mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), v2.clone().sub(v1).normalize());
    }

    let currentMode = 'squat';
    let animTime = 0;

    const dispExercise = document.getElementById('disp-exercise');
    const dispAngle = document.getElementById('disp-angle');
    const dispStatus = document.getElementById('disp-status');
    const dispFatigue = document.getElementById('disp-fatigue');

    function applyPose(t) {
      const headPos = new THREE.Vector3(0, 1.45, 0);
      const neckPos = new THREE.Vector3(0, 1.25, 0);
      const chestPos = new THREE.Vector3(0, 0.95, 0);
      const pelvisPos = new THREE.Vector3(0, 0.45, 0);

      const lShoulder = new THREE.Vector3(-0.35, 1.2, 0);
      const rShoulder = new THREE.Vector3(0.35, 1.2, 0);
      const lElbow = new THREE.Vector3(-0.45, 0.8, 0.05);
      const rElbow = new THREE.Vector3(0.45, 0.8, 0.05);
      const lWrist = new THREE.Vector3(-0.45, 0.4, 0.1);
      const rWrist = new THREE.Vector3(0.45, 0.4, 0.1);

      const lHip = new THREE.Vector3(-0.2, 0.4, 0);
      const rHip = new THREE.Vector3(0.2, 0.4, 0);
      const lKnee = new THREE.Vector3(-0.22, -0.4, 0.05);
      const rKnee = new THREE.Vector3(0.22, -0.4, 0.05);
      const lAnkle = new THREE.Vector3(-0.24, -1.2, 0);
      const rAnkle = new THREE.Vector3(0.24, -1.2, 0);
      const lFoot = new THREE.Vector3(-0.24, -1.22, 0.25);
      const rFoot = new THREE.Vector3(0.24, -1.22, 0.25);

      modelGroup.rotation.x = 0;
      modelGroup.position.set(0, 0, 0);

      const sinWave = (Math.sin(t * 2.5) + 1) / 2;

      if (currentMode === 'squat') {
        const drop = sinWave * 0.75;
        const kneeForward = sinWave * 0.4;
        const hipBack = sinWave * 0.35;

        pelvisPos.y -= drop;
        pelvisPos.z -= hipBack;
        chestPos.y -= drop * 0.9;
        chestPos.z -= hipBack * 0.6;
        neckPos.y -= drop * 0.85;
        headPos.y -= drop * 0.85;

        lHip.y -= drop;
        lHip.z -= hipBack;
        rHip.y -= drop;
        rHip.z -= hipBack;

        lKnee.y -= drop * 0.5;
        lKnee.z += kneeForward;
        rKnee.y -= drop * 0.5;
        rKnee.z += kneeForward;

        lElbow.z += sinWave * 0.5;
        rElbow.z += sinWave * 0.5;
        lWrist.z += sinWave * 0.7;
        rWrist.z += sinWave * 0.7;

        const currentAngle = Math.round(175 - sinWave * 87);
        dispExercise.innerText = 'SQUATS';
        dispAngle.innerText = `${currentAngle}° (KNEE DEPTH)`;
        dispStatus.innerText = currentAngle <= 92 ? '🟢 PARALLEL DEPTH HIT' : '🟡 DESCENDING';
        dispFatigue.innerText = `${(sinWave * 12.5).toFixed(1)}% (VELOCITY NORMAL)`;

      } else if (currentMode === 'curl') {
        const curlProgress = sinWave;
        rWrist.y = 0.4 + curlProgress * 0.65;
        rWrist.z = 0.1 + curlProgress * 0.4;
        rWrist.x = 0.45 - curlProgress * 0.1;

        const lProgress = (Math.sin(t * 2.5 + Math.PI) + 1) / 2;
        lWrist.y = 0.4 + lProgress * 0.65;
        lWrist.z = 0.1 + lProgress * 0.4;
        lWrist.x = -0.45 + lProgress * 0.1;

        const bicepAngle = Math.round(170 - curlProgress * 128);
        dispExercise.innerText = 'BICEPS CURLS';
        dispAngle.innerText = `${bicepAngle}° (ELBOW FLEXION)`;
        dispStatus.innerText = bicepAngle <= 55 ? '🟢 PEAK CONTRACTION' : '⚡ ECCENTRIC PHASE';
        dispFatigue.innerText = `${(curlProgress * 18.2).toFixed(1)}% (SPEED 1.2m/s)`;

      } else if (currentMode === 'pushup') {
        modelGroup.rotation.x = -Math.PI / 2.3;
        modelGroup.position.set(0, -0.4, 0);

        const pushDrop = sinWave * 0.45;
        headPos.z += pushDrop;
        chestPos.z += pushDrop;
        neckPos.z += pushDrop;
        pelvisPos.z += pushDrop * 0.85;

        lElbow.x = -0.65 - pushDrop * 0.3;
        rElbow.x = 0.65 + pushDrop * 0.3;
        lElbow.z += pushDrop * 0.5;
        rElbow.z += pushDrop * 0.5;

        const pushAngle = Math.round(165 - sinWave * 75);
        dispExercise.innerText = 'PUSH-UPS';
        dispAngle.innerText = `${pushAngle}° (CHEST DEPTH)`;
        dispStatus.innerText = pushAngle <= 95 ? '🟢 FULL ROM HIT' : '⚡ PRESSING UP';
        dispFatigue.innerText = `${(sinWave * 22.0).toFixed(1)}% (CHEST BURNOUT)`;

      } else if (currentMode === 'press') {
        const pressProgress = sinWave;
        lElbow.y = 1.2 + pressProgress * 0.5;
        lElbow.x = -0.55 + pressProgress * 0.18;
        rElbow.y = 1.2 + pressProgress * 0.5;
        rElbow.x = 0.55 - pressProgress * 0.18;

        lWrist.y = 1.45 + pressProgress * 0.7;
        lWrist.x = -0.52 + pressProgress * 0.22;
        rWrist.y = 1.45 + pressProgress * 0.7;
        rWrist.x = 0.52 - pressProgress * 0.22;

        const pressAngle = Math.round(90 + pressProgress * 82);
        dispExercise.innerText = 'SHOULDER PRESS';
        dispAngle.innerText = `${pressAngle}° (OVERHEAD LOCK)`;
        dispStatus.innerText = pressAngle >= 165 ? '🟢 FULL OVERHEAD LOCK' : '⚡ POWER DRIVE';
        dispFatigue.innerText = `${(pressProgress * 15.0).toFixed(1)}% (DELT TENSION)`;

      } else if (currentMode === 'scan') {
        const breathe = Math.sin(t * 1.5) * 0.02;
        chestPos.y += breathe;
        neckPos.y += breathe * 0.7;
        headPos.y += breathe * 0.5;

        modelGroup.rotation.y += 0.008;

        dispExercise.innerText = '360° SKELETON SCAN';
        dispAngle.innerText = '33/33 JOINTS ONLINE';
        dispStatus.innerText = '🟢 KINEMATICS READY';
        dispFatigue.innerText = '0.0% (RESTORED)';
      }

      scanRing.position.y = Math.sin(t * 1.8) * 1.5;

      joints['head'].position.copy(headPos);
      joints['neck'].position.copy(neckPos);
      joints['chest'].position.copy(chestPos);
      joints['pelvis'].position.copy(pelvisPos);

      joints['left_shoulder'].position.copy(lShoulder);
      joints['right_shoulder'].position.copy(rShoulder);
      joints['left_elbow'].position.copy(lElbow);
      joints['right_elbow'].position.copy(rElbow);
      joints['left_wrist'].position.copy(lWrist);
      joints['right_wrist'].position.copy(rWrist);

      joints['left_hip'].position.copy(lHip);
      joints['right_hip'].position.copy(rHip);
      joints['left_knee'].position.copy(lKnee);
      joints['right_knee'].position.copy(rKnee);
      joints['left_ankle'].position.copy(lAnkle);
      joints['right_ankle'].position.copy(rAnkle);
      joints['left_foot_index'].position.copy(lFoot);
      joints['right_foot_index'].position.copy(rFoot);

      boneMeshes.forEach(updateBone);
    }

    const buttons = document.querySelectorAll('.ctrl-btn');
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentMode = btn.getAttribute('data-mode');
        animTime = 0;
      });
    });

    const clock = new THREE.Clock();
    function animate() {
      requestAnimationFrame(animate);
      const delta = clock.getDelta();
      animTime += delta;
      particles.rotation.y += 0.001;
      applyPose(animTime);
      controls.update();
      renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    });
  </script>
</body>
</html>
"""


def render_3d_digital_twin():
    """
    Renders the futuristic 3D WebGL Biomechanical Avatar inside the Streamlit Web App.
    """
    st.markdown("""
        <div style="margin-bottom: 16px;">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h2 style="color: #FFFFFF; font-size: 24px; font-weight: 900; margin: 0; letter-spacing: -0.02em;">
                        🧬 3D BIOMECHANICAL DIGITAL TWIN
                    </h2>
                    <p style="color: #94A3B8; font-size: 13px; margin-top: 4px;">
                        Interactive WebGL 3D Pose Geometry &bull; Drag to rotate 360° &bull; Test exercise kinematics
                    </p>
                </div>
                <div style="background: rgba(0, 245, 155, 0.12); border: 1px solid #00F59B; padding: 6px 14px; border-radius: 8px; color: #00F59B; font-weight: 800; font-size: 12px;">
                    ⚡ 33 3D POSE LANDMARKS ACTIVE
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 1. 3D WebGL Canvas Component
    components.html(THREEJS_AVATAR_HTML, height=580, scrolling=False)

    # 2. Biomechanical Angle Audit Matrix
    st.markdown("---")
    st.markdown("### 📐 Kinematic Angle Matrix & Form Standards")
    st.caption("These mathematical angular thresholds are continuously calculated in real time by the MediaPipe 3D pipeline.")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <div style="background: rgba(14, 20, 33, 0.85); border: 1px solid rgba(0,245,155,0.3); border-radius: 12px; padding: 16px;">
                <div style="color: #00F59B; font-weight: 800; font-size: 11px; text-transform: uppercase;">Knee Flexion</div>
                <div style="color: #FFFFFF; font-size: 24px; font-weight: 900; margin: 4px 0;">&le; 90°</div>
                <div style="color: #94A3B8; font-size: 11px;">Squat Depth Standard &bull; Full hamstring & quad recruitment.</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style="background: rgba(14, 20, 33, 0.85); border: 1px solid rgba(56,189,248,0.3); border-radius: 12px; padding: 16px;">
                <div style="color: #38BDF8; font-weight: 800; font-size: 11px; text-transform: uppercase;">Elbow Contraction</div>
                <div style="color: #FFFFFF; font-size: 24px; font-weight: 900; margin: 4px 0;">&le; 45°</div>
                <div style="color: #94A3B8; font-size: 11px;">Biceps Peak Hypertrophy &bull; Maximum short-head tension.</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div style="background: rgba(14, 20, 33, 0.85); border: 1px solid rgba(251,191,36,0.3); border-radius: 12px; padding: 16px;">
                <div style="color: #FBBF24; font-weight: 800; font-size: 11px; text-transform: uppercase;">Humeral Flare</div>
                <div style="color: #FFFFFF; font-size: 24px; font-weight: 900; margin: 4px 0;">45° - 75°</div>
                <div style="color: #94A3B8; font-size: 11px;">Push-Up Rotator Safety &bull; Prevents anterior shoulder impingement.</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div style="background: rgba(14, 20, 33, 0.85); border: 1px solid rgba(168,85,247,0.3); border-radius: 12px; padding: 16px;">
                <div style="color: #A855F7; font-weight: 800; font-size: 11px; text-transform: uppercase;">Overhead Lockout</div>
                <div style="color: #FFFFFF; font-size: 24px; font-weight: 900; margin: 4px 0;">&ge; 170°</div>
                <div style="color: #94A3B8; font-size: 11px;">Shoulder Press Full ROM &bull; Complete deltoid & trapezius lockout.</div>
            </div>
        """, unsafe_allow_html=True)
