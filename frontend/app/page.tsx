"use client";

import { useState, useRef, useEffect } from "react";
import {
  PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend
} from "recharts";

// ─── Types ───────────────────────────────────────────────────────────────────

interface WorkforceInputs {
  hiringTarget: number;
  companyType: "product" | "consulting" | "gcc" | "startup" | "enterprise";
  dropoutRatio: number;
  complexityFactor: "low" | "medium" | "high" | "hyper";
  recruiterProductivity: number;
  geography: "domestic" | "multi-region" | "global";
  aiNichePercent: number;
}

interface TAStructure {
  adjustedHiring: number;
  totalTA: number;
  juniorRecruiters: number;
  recruiters: number;
  seniorRecruiters: number;
  sourcers: number;
  coordinators: number;
  leads: number;
  managers: number;
  taHead: number;
  hiringCapacity: number;
  timeline: string;
  utilization: number;
  estimatedCost: string;
}

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

// ─── Calculation Engine ───────────────────────────────────────────────────────

function calculateTAStructure(inputs: WorkforceInputs): TAStructure {
  const {
    hiringTarget, companyType, dropoutRatio,
    complexityFactor, recruiterProductivity, aiNichePercent
  } = inputs;

  const adjustedHiring = Math.ceil(hiringTarget / (1 - dropoutRatio / 100));

  const complexityMap = {
    low: 1.0, medium: 1.1, high: 1.2, hyper: 1.4
  };
  const cf = complexityMap[complexityFactor];

  const aiBoost = 1 + (aiNichePercent / 100) * 0.3;

  let baseProductivity = recruiterProductivity;
  let coreRecruiters: number;

  if (companyType === "product" || companyType === "gcc" || companyType === "startup") {
    coreRecruiters = Math.ceil((adjustedHiring * cf * aiBoost) / baseProductivity);
    const juniorRecruiters = Math.round(coreRecruiters * 0.40);
    const recruiters = Math.round(coreRecruiters * 0.35);
    const seniorRecruiters = Math.round(coreRecruiters * 0.25);
    const sourcers = Math.ceil(coreRecruiters / 4);
    const coordinators = Math.ceil(coreRecruiters / 7);
    const leads = Math.ceil(coreRecruiters / 5);
    const managers = Math.ceil(leads / 3);
    const taHead = 1;
    const totalTA = juniorRecruiters + recruiters + seniorRecruiters + sourcers + coordinators + leads + managers + taHead;
    const hiringCapacity = Math.round(coreRecruiters * baseProductivity / cf);
    const months = Math.ceil(adjustedHiring / (coreRecruiters * (baseProductivity / 12)));
    const utilization = Math.min(98, Math.round((adjustedHiring / hiringCapacity) * 100));
    const avgSalary = companyType === "product" ? 1800000 : 1400000;
    const totalCost = totalTA * avgSalary;
    return {
      adjustedHiring, totalTA, juniorRecruiters, recruiters, seniorRecruiters,
      sourcers, coordinators, leads, managers, taHead, hiringCapacity,
      timeline: `${months}–${months + 2} months`, utilization,
      estimatedCost: `₹${(totalCost / 100000).toFixed(1)}L/yr`
    };
  } else {
    baseProductivity = companyType === "enterprise" ? 45 : 55;
    const volumeMap = { low: 1.0, medium: 1.1, high: 1.2, hyper: 1.25 };
    const vf = volumeMap[complexityFactor];
    coreRecruiters = Math.ceil((adjustedHiring * vf) / baseProductivity);
    const juniorRecruiters = Math.round(coreRecruiters * 0.50);
    const recruiters = Math.round(coreRecruiters * 0.35);
    const seniorRecruiters = Math.round(coreRecruiters * 0.15);
    const sourcers = Math.ceil(coreRecruiters / 5);
    const coordinators = Math.ceil(coreRecruiters / 8);
    const leads = Math.ceil(coreRecruiters / 6);
    const managers = Math.ceil(leads / 3);
    const taHead = 1;
    const totalTA = juniorRecruiters + recruiters + seniorRecruiters + sourcers + coordinators + leads + managers + taHead;
    const hiringCapacity = Math.round(coreRecruiters * baseProductivity);
    const months = Math.ceil(adjustedHiring / (coreRecruiters * (baseProductivity / 12)));
    const utilization = Math.min(98, Math.round((adjustedHiring / hiringCapacity) * 100));
    const totalCost = totalTA * 1200000;
    return {
      adjustedHiring, totalTA, juniorRecruiters, recruiters, seniorRecruiters,
      sourcers, coordinators, leads, managers, taHead, hiringCapacity,
      timeline: `${months}–${months + 2} months`, utilization,
      estimatedCost: `₹${(totalCost / 100000).toFixed(1)}L/yr`
    };
  }
}

// ─── Color Palette ────────────────────────────────────────────────────────────

const COLORS = ["#1a1a2e", "#16213e", "#0f3460", "#533483", "#7b2d8b", "#e94560", "#f5a623", "#00d4aa"];

// ─── Sub-components ───────────────────────────────────────────────────────────

function MetricCard({ label, value, sub, accent }: { label: string; value: string | number; sub?: string; accent?: string }) {
  return (
    <div style={{
      background: "white", border: "1px solid #f0f0f0", borderRadius: 12,
      padding: "14px 16px", position: "relative", overflow: "hidden"
    }}>
      {accent && <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: 3, background: accent, borderRadius: "12px 0 0 12px" }} />}
      <div style={{ fontSize: 11, color: "#9ca3af", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 4 }}>{label}</div>
      <div style={{ fontSize: 22, fontWeight: 700, color: "#111", lineHeight: 1 }}>{value}</div>
      {sub && <div style={{ fontSize: 11, color: "#9ca3af", marginTop: 4 }}>{sub}</div>}
    </div>
  );
}

function TypingDots() {
  return (
    <span style={{ display: "inline-flex", gap: 3, alignItems: "center", padding: "4px 0" }}>
      {[0, 1, 2].map(i => (
        <span key={i} style={{
          width: 6, height: 6, borderRadius: "50%", background: "#6b7280",
          animation: "bounce 1.2s infinite", animationDelay: `${i * 0.2}s`
        }} />
      ))}
      <style>{`@keyframes bounce{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-6px)}}`}</style>
    </span>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────

export default function TalentScaleAI() {
  const [inputs, setInputs] = useState<WorkforceInputs>({
    hiringTarget: 600,
    companyType: "product",
    dropoutRatio: 25,
    complexityFactor: "medium",
    recruiterProductivity: 32,
    geography: "domestic",
    aiNichePercent: 30
  });

  const [result, setResult] = useState<TAStructure | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([{
    role: "assistant",
    content: "👋 Hi! I'm your AI Workforce Planning Assistant. Enter your hiring parameters and click **Calculate**, then ask me anything about your TA structure, recruiter benchmarks, or hiring strategy."
  }]);
  const [chatInput, setChatInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isCalculating, setIsCalculating] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleCalculate = async () => {
    setIsCalculating(true);
    await new Promise(r => setTimeout(r, 600));
    const res = calculateTAStructure(inputs);
    setResult(res);
    setIsCalculating(false);

    const summary = `✅ Calculation complete! For **${inputs.hiringTarget} hires** at a **${inputs.companyType.toUpperCase()}** company with **${inputs.dropoutRatio}% dropout**, you need a team of **${res.totalTA} TA professionals**. That includes ${res.recruiters} core Recruiters, ${res.seniorRecruiters} Senior Recruiters, ${res.juniorRecruiters} Junior Recruiters, and ${res.leads} Team Leads. Estimated timeline: **${res.timeline}**. Ask me anything to dig deeper!`;
    setMessages(prev => [...prev, { role: "assistant", content: summary }]);
  };

  const handleSend = async () => {
    if (!chatInput.trim() || isLoading) return;
    const userMsg = chatInput.trim();
    setChatInput("");
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    setIsLoading(true);

    try {
      const systemPrompt = `You are TalentScale AI, an expert HR workforce planning assistant specializing in Talent Acquisition team structures for Indian and global tech companies.

Current calculation context:
${result ? `
- Hiring Target: ${inputs.hiringTarget} (Adjusted: ${result.adjustedHiring})
- Company Type: ${inputs.companyType}
- Dropout Ratio: ${inputs.dropoutRatio}%
- Complexity: ${inputs.complexityFactor}
- Recruiter Productivity: ${inputs.recruiterProductivity}
- AI/Niche Hiring: ${inputs.aiNichePercent}%
- Total TA Team: ${result.totalTA}
- Junior Recruiters: ${result.juniorRecruiters}
- Recruiters: ${result.recruiters}
- Senior Recruiters: ${result.seniorRecruiters}
- Sourcers: ${result.sourcers}
- Coordinators: ${result.coordinators}
- Leads: ${result.leads}
- Managers: ${result.managers}
- TA Head: ${result.taHead}
- Timeline: ${result.timeline}
- Utilization: ${result.utilization}%
- Estimated Cost: ${result.estimatedCost}
` : "No calculation done yet."}

Provide concise, expert advice. Use industry benchmarks (Naukri, LinkedIn India data). Be specific with numbers. Keep answers under 150 words. Use markdown for formatting.`;

     await new Promise(r => setTimeout(r, 1000));

setMessages(prev => [
  ...prev,
  {
    role: "assistant",
    content:
      "AI backend will be connected after backend deployment."
  }
]);, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: systemPrompt,
          messages: [
            ...messages.filter(m => m.role !== "assistant" || messages.indexOf(m) > 0).slice(-6).map(m => ({
              role: m.role,
              content: m.content
            })),
            { role: "user", content: userMsg }
          ]
        })
      });
      const data = await response.json();
      const reply = data.content?.[0]?.text || "I encountered an error. Please try again.";
      setMessages(prev => [...prev, { role: "assistant", content: reply }]);
    } catch {
      setMessages(prev => [...prev, { role: "assistant", content: "Connection error. Please check your setup and try again." }]);
    }
    setIsLoading(false);
  };

  const pieData = result ? [
    { name: "Junior Rec.", value: result.juniorRecruiters },
    { name: "Recruiters", value: result.recruiters },
    { name: "Senior Rec.", value: result.seniorRecruiters },
    { name: "Sourcers", value: result.sourcers },
    { name: "Coordinators", value: result.coordinators },
    { name: "Leads", value: result.leads },
    { name: "Managers", value: result.managers },
    { name: "TA Head", value: result.taHead }
  ] : [];

  const barData = result ? [
    { role: "Jr. Rec.", count: result.juniorRecruiters },
    { role: "Recruiter", count: result.recruiters },
    { role: "Sr. Rec.", count: result.seniorRecruiters },
    { role: "Sourcer", count: result.sourcers },
    { role: "Coord.", count: result.coordinators },
    { role: "Lead", count: result.leads },
    { role: "Manager", count: result.managers },
  ] : [];

  const renderMarkdown = (text: string) => {
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br/>');
  };

  return (
    <div style={{ minHeight: "100vh", background: "#f8f9fc", fontFamily: "'DM Sans', system-ui, sans-serif" }}>
      {/* Header */}
      <header style={{
        background: "white", borderBottom: "1px solid #e5e7eb",
        padding: "0 24px", height: 60, display: "flex", alignItems: "center",
        justifyContent: "space-between", position: "sticky", top: 0, zIndex: 100,
        boxShadow: "0 1px 3px rgba(0,0,0,0.05)"
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{
            width: 32, height: 32, borderRadius: 8,
            background: "linear-gradient(135deg, #1a1a2e 0%, #533483 100%)",
            display: "flex", alignItems: "center", justifyContent: "center"
          }}>
            <span style={{ color: "white", fontWeight: 800, fontSize: 14 }}>T</span>
          </div>
          <div>
            <div style={{ fontWeight: 700, fontSize: 15, color: "#111", lineHeight: 1.2 }}>TalentScale AI</div>
            <div style={{ fontSize: 10, color: "#9ca3af", letterSpacing: "0.05em" }}>WORKFORCE PLANNING</div>
          </div>
        </div>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <button style={{
            padding: "6px 14px", borderRadius: 8, border: "1px solid #e5e7eb",
            background: "white", fontSize: 12, color: "#374151", cursor: "pointer",
            fontWeight: 500, display: "flex", alignItems: "center", gap: 5
          }}>
            ↓ Export
          </button>
          <div style={{
            width: 32, height: 32, borderRadius: "50%",
            background: "linear-gradient(135deg, #533483, #e94560)",
            display: "flex", alignItems: "center", justifyContent: "center",
            color: "white", fontSize: 12, fontWeight: 700
          }}>HR</div>
        </div>
      </header>

      {/* Main Grid */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "280px 1fr 340px",
        gap: 16,
        padding: 16,
        maxWidth: 1400,
        margin: "0 auto",
        height: "calc(100vh - 76px)"
      }}>

        {/* LEFT: Input Panel */}
        <div style={{
          background: "white", borderRadius: 16, border: "1px solid #e5e7eb",
          padding: 20, overflowY: "auto", display: "flex", flexDirection: "column", gap: 12
        }}>
          <div style={{ fontWeight: 700, fontSize: 14, color: "#111", marginBottom: 4 }}>
            Workforce Inputs
          </div>

          {/* Total Hiring Target */}
          <div>
            <label style={{ fontSize: 11, color: "#6b7280", fontWeight: 500, display: "block", marginBottom: 4 }}>
              TOTAL HIRING TARGET
            </label>
            <input type="number" value={inputs.hiringTarget}
              onChange={e => setInputs(p => ({ ...p, hiringTarget: +e.target.value }))}
              style={{
                width: "100%", padding: "8px 10px", borderRadius: 8, border: "1px solid #e5e7eb",
                fontSize: 14, color: "#111", outline: "none", boxSizing: "border-box"
              }} />
          </div>

          {/* Company Type */}
          <div>
            <label style={{ fontSize: 11, color: "#6b7280", fontWeight: 500, display: "block", marginBottom: 4 }}>
              COMPANY TYPE
            </label>
            <select value={inputs.companyType}
              onChange={e => setInputs(p => ({ ...p, companyType: e.target.value as WorkforceInputs["companyType"] }))}
              style={{
                width: "100%", padding: "8px 10px", borderRadius: 8, border: "1px solid #e5e7eb",
                fontSize: 13, color: "#111", outline: "none", background: "white", boxSizing: "border-box"
              }}>
              <option value="product">IT Product Company</option>
              <option value="consulting">IT Consulting Company</option>
              <option value="gcc">GCC</option>
              <option value="startup">Startup</option>
              <option value="enterprise">Enterprise</option>
            </select>
          </div>

          {/* Dropout Ratio */}
          <div>
            <label style={{ fontSize: 11, color: "#6b7280", fontWeight: 500, display: "block", marginBottom: 4 }}>
              DROPOUT RATIO: {inputs.dropoutRatio}%
            </label>
            <input type="range" min={5} max={50} value={inputs.dropoutRatio}
              onChange={e => setInputs(p => ({ ...p, dropoutRatio: +e.target.value }))}
              style={{ width: "100%" }} />
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 10, color: "#9ca3af" }}>
              <span>5%</span><span>50%</span>
            </div>
          </div>

          {/* Complexity */}
          <div>
            <label style={{ fontSize: 11, color: "#6b7280", fontWeight: 500, display: "block", marginBottom: 6 }}>
              HIRING COMPLEXITY
            </label>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 6 }}>
              {(["low", "medium", "high", "hyper"] as const).map(c => (
                <button key={c} onClick={() => setInputs(p => ({ ...p, complexityFactor: c }))}
                  style={{
                    padding: "7px 4px", borderRadius: 8, border: "1.5px solid",
                    borderColor: inputs.complexityFactor === c ? "#533483" : "#e5e7eb",
                    background: inputs.complexityFactor === c ? "#f5f0ff" : "white",
                    color: inputs.complexityFactor === c ? "#533483" : "#6b7280",
                    fontSize: 11, fontWeight: 600, cursor: "pointer",
                    textTransform: "capitalize"
                  }}>
                  {c === "hyper" ? "Hyper Niche" : c.charAt(0).toUpperCase() + c.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Recruiter Productivity */}
          <div>
            <label style={{ fontSize: 11, color: "#6b7280", fontWeight: 500, display: "block", marginBottom: 4 }}>
              RECRUITER PRODUCTIVITY
            </label>
            <input type="number" value={inputs.recruiterProductivity}
              onChange={e => setInputs(p => ({ ...p, recruiterProductivity: +e.target.value }))}
              style={{
                width: "100%", padding: "8px 10px", borderRadius: 8, border: "1px solid #e5e7eb",
                fontSize: 14, color: "#111", outline: "none", boxSizing: "border-box"
              }} />
            <div style={{ fontSize: 10, color: "#9ca3af", marginTop: 3 }}>Hires per recruiter per year</div>
          </div>

          {/* Geography */}
          <div>
            <label style={{ fontSize: 11, color: "#6b7280", fontWeight: 500, display: "block", marginBottom: 4 }}>
              HIRING GEOGRAPHY
            </label>
            <select value={inputs.geography}
              onChange={e => setInputs(p => ({ ...p, geography: e.target.value as WorkforceInputs["geography"] }))}
              style={{
                width: "100%", padding: "8px 10px", borderRadius: 8, border: "1px solid #e5e7eb",
                fontSize: 13, color: "#111", outline: "none", background: "white", boxSizing: "border-box"
              }}>
              <option value="domestic">Domestic Only</option>
              <option value="multi-region">Multi-Region</option>
              <option value="global">Global</option>
            </select>
          </div>

          {/* AI/Niche % */}
          <div>
            <label style={{ fontSize: 11, color: "#6b7280", fontWeight: 500, display: "block", marginBottom: 4 }}>
              AI / NICHE HIRING %: {inputs.aiNichePercent}%
            </label>
            <input type="range" min={0} max={80} value={inputs.aiNichePercent}
              onChange={e => setInputs(p => ({ ...p, aiNichePercent: +e.target.value }))}
              style={{ width: "100%" }} />
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 10, color: "#9ca3af" }}>
              <span>0%</span><span>80%</span>
            </div>
          </div>

          {/* Calculate Button */}
          <button onClick={handleCalculate} disabled={isCalculating}
            style={{
              padding: "12px", borderRadius: 10, border: "none",
              background: isCalculating ? "#c4b5fd" : "linear-gradient(135deg, #1a1a2e 0%, #533483 100%)",
              color: "white", fontSize: 13, fontWeight: 700, cursor: isCalculating ? "not-allowed" : "pointer",
              width: "100%", marginTop: 4, letterSpacing: "0.03em"
            }}>
            {isCalculating ? "Calculating..." : "⚡ Calculate TA Structure"}
          </button>
        </div>

        {/* CENTER: Output Panel */}
        <div style={{
          background: "white", borderRadius: 16, border: "1px solid #e5e7eb",
          padding: 20, overflowY: "auto"
        }}>
          <div style={{ fontWeight: 700, fontSize: 14, color: "#111", marginBottom: 16 }}>
            Recommended TA Structure
            {result && <span style={{
              marginLeft: 8, fontSize: 11, background: "#f0fdf4", color: "#16a34a",
              padding: "2px 8px", borderRadius: 20, fontWeight: 600
            }}>● Calculated</span>}
          </div>

          {!result ? (
            <div style={{
              display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
              height: 300, color: "#d1d5db", gap: 12
            }}>
              <div style={{ fontSize: 40 }}>📊</div>
              <div style={{ fontSize: 13, textAlign: "center" }}>
                Enter your hiring parameters<br />and click Calculate
              </div>
            </div>
          ) : (
            <>
              {/* Primary Metrics */}
              <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 10, marginBottom: 16 }}>
                <MetricCard label="Total TA Team" value={result.totalTA} sub="headcount" accent="#533483" />
                <MetricCard label="Hiring Capacity" value={result.hiringCapacity} sub="hires/year" accent="#e94560" />
                <MetricCard label="Utilization" value={`${result.utilization}%`} sub="recruiter load" accent="#f5a623" />
                <MetricCard label="Est. TA Cost" value={result.estimatedCost} sub="annual" accent="#00d4aa" />
              </div>

              {/* Timeline */}
              <div style={{
                background: "#f8f9fc", borderRadius: 10, padding: "10px 14px",
                display: "flex", alignItems: "center", gap: 10, marginBottom: 16,
                border: "1px solid #e5e7eb"
              }}>
                <span style={{ fontSize: 20 }}>⏱</span>
                <div>
                  <div style={{ fontSize: 11, color: "#9ca3af" }}>Estimated Hiring Timeline</div>
                  <div style={{ fontWeight: 700, color: "#111" }}>{result.timeline}</div>
                </div>
                <div style={{ marginLeft: "auto", textAlign: "right" }}>
                  <div style={{ fontSize: 11, color: "#9ca3af" }}>Adjusted Target</div>
                  <div style={{ fontWeight: 700, color: "#533483" }}>{result.adjustedHiring} hires</div>
                </div>
              </div>

              {/* Role Cards */}
              <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 8, marginBottom: 20 }}>
                {[
                  { label: "Junior Recruiters", value: result.juniorRecruiters, color: "#e0f2fe", text: "#0369a1" },
                  { label: "Recruiters", value: result.recruiters, color: "#ede9fe", text: "#533483" },
                  { label: "Senior Recruiters", value: result.seniorRecruiters, color: "#fce7f3", text: "#be185d" },
                  { label: "Sourcers", value: result.sourcers, color: "#fef3c7", text: "#92400e" },
                  { label: "Coordinators", value: result.coordinators, color: "#d1fae5", text: "#065f46" },
                  { label: "Team Leads", value: result.leads, color: "#ffe4e6", text: "#9f1239" },
                  { label: "Managers", value: result.managers, color: "#f3f4f6", text: "#374151" },
                  { label: "TA Head", value: result.taHead, color: "#1a1a2e", text: "white" },
                ].map(item => (
                  <div key={item.label} style={{
                    background: item.color, borderRadius: 10, padding: "10px 12px",
                    display: "flex", justifyContent: "space-between", alignItems: "center"
                  }}>
                    <div style={{ fontSize: 11, color: item.text, fontWeight: 500 }}>{item.label}</div>
                    <div style={{ fontSize: 20, fontWeight: 800, color: item.text }}>{item.value}</div>
                  </div>
                ))}
              </div>

              {/* Charts */}
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
                <div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: "#6b7280", marginBottom: 8 }}>Team Distribution</div>
                  <ResponsiveContainer width="100%" height={200}>
                    <PieChart>
                      <Pie data={pieData} cx="50%" cy="50%" innerRadius={50} outerRadius={80}
                        dataKey="value" paddingAngle={2}>
                        {pieData.map((_, i) => (
                          <Cell key={i} fill={COLORS[i % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip formatter={(v: number) => [v, "Count"]} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                <div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: "#6b7280", marginBottom: 8 }}>Headcount by Role</div>
                  <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={barData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                      <XAxis dataKey="role" tick={{ fontSize: 10 }} />
                      <YAxis tick={{ fontSize: 10 }} />
                      <Tooltip />
                      <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                        {barData.map((_, i) => (
                          <Cell key={i} fill={COLORS[i % COLORS.length]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </>
          )}
        </div>

        {/* RIGHT: Chat Panel */}
        <div style={{
          background: "white", borderRadius: 16, border: "1px solid #e5e7eb",
          display: "flex", flexDirection: "column", overflow: "hidden"
        }}>
          <div style={{
            padding: "14px 16px", borderBottom: "1px solid #f3f4f6",
            display: "flex", alignItems: "center", gap: 8
          }}>
            <div style={{
              width: 28, height: 28, borderRadius: 8,
              background: "linear-gradient(135deg, #533483, #e94560)",
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: 12
            }}>✦</div>
            <div>
              <div style={{ fontWeight: 700, fontSize: 13, color: "#111" }}>AI Workforce Planning Assistant</div>
              <div style={{ fontSize: 10, color: "#22c55e", display: "flex", alignItems: "center", gap: 3 }}>
                <span style={{ width: 5, height: 5, borderRadius: "50%", background: "#22c55e", display: "inline-block" }} />
                Online
              </div>
            </div>
          </div>

          {/* Messages */}
          <div style={{ flex: 1, overflowY: "auto", padding: "12px 14px", display: "flex", flexDirection: "column", gap: 10 }}>
            {messages.map((msg, i) => (
              <div key={i} style={{
                display: "flex", justifyContent: msg.role === "user" ? "flex-end" : "flex-start",
                gap: 8, alignItems: "flex-end"
              }}>
                {msg.role === "assistant" && (
                  <div style={{
                    width: 24, height: 24, borderRadius: 6, flexShrink: 0,
                    background: "linear-gradient(135deg, #533483, #e94560)",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: 10, color: "white"
                  }}>✦</div>
                )}
                <div style={{
                  maxWidth: "82%", padding: "9px 12px", borderRadius: 12,
                  background: msg.role === "user" ? "#1a1a2e" : "#f8f9fc",
                  color: msg.role === "user" ? "white" : "#111",
                  fontSize: 12.5, lineHeight: 1.5,
                  borderBottomRightRadius: msg.role === "user" ? 4 : 12,
                  borderBottomLeftRadius: msg.role === "assistant" ? 4 : 12,
                }}
                  dangerouslySetInnerHTML={{ __html: renderMarkdown(msg.content) }}
                />
              </div>
            ))}
            {isLoading && (
              <div style={{ display: "flex", gap: 8, alignItems: "flex-end" }}>
                <div style={{
                  width: 24, height: 24, borderRadius: 6, flexShrink: 0,
                  background: "linear-gradient(135deg, #533483, #e94560)",
                  display: "flex", alignItems: "center", justifyContent: "center",
                  fontSize: 10, color: "white"
                }}>✦</div>
                <div style={{ padding: "9px 14px", background: "#f8f9fc", borderRadius: 12 }}>
                  <TypingDots />
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          {/* Quick Prompts */}
          <div style={{ padding: "6px 12px", display: "flex", gap: 5, flexWrap: "wrap", borderTop: "1px solid #f3f4f6" }}>
            {[
              "Why so many recruiters?",
              "Industry benchmarks",
              "Cost breakdown",
              "Reduce timeline"
            ].map(q => (
              <button key={q} onClick={() => { setChatInput(q); }}
                style={{
                  padding: "4px 10px", borderRadius: 20, border: "1px solid #e5e7eb",
                  background: "white", fontSize: 10.5, color: "#6b7280", cursor: "pointer",
                  whiteSpace: "nowrap"
                }}>
                {q}
              </button>
            ))}
          </div>

          {/* Input Box */}
          <div style={{
            padding: "10px 12px", borderTop: "1px solid #f3f4f6",
            display: "flex", gap: 8, alignItems: "flex-end"
          }}>
            <textarea value={chatInput}
              onChange={e => setChatInput(e.target.value)}
              onKeyDown={e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); } }}
              placeholder="Ask about your TA structure..."
              rows={2}
              style={{
                flex: 1, padding: "8px 10px", borderRadius: 10, border: "1px solid #e5e7eb",
                fontSize: 12.5, resize: "none", outline: "none", color: "#111",
                fontFamily: "inherit", lineHeight: 1.4
              }} />
            <button onClick={handleSend} disabled={isLoading || !chatInput.trim()}
              style={{
                width: 36, height: 36, borderRadius: 9, border: "none",
                background: chatInput.trim() ? "linear-gradient(135deg, #533483, #e94560)" : "#e5e7eb",
                color: "white", cursor: chatInput.trim() ? "pointer" : "not-allowed",
                fontSize: 14, display: "flex", alignItems: "center", justifyContent: "center",
                flexShrink: 0
              }}>↑</button>
          </div>
        </div>
      </div>
    </div>
  );
}
