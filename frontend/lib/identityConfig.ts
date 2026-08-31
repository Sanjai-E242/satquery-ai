export interface TeamMember {
  name: string;
  role: string;
  avatarBg?: string;
  skills?: string[];
}

export interface IdentityConfig {
  PROJECT_NAME: string;
  TAGLINE: string;
  DEVELOPED_BY: string;
  DEVELOPER_ROLE: string;
  COLLEGE_NAME: string;
  DEPARTMENT: string;
  TEAM_NAME: string;
  TEAM_MEMBERS: TeamMember[];
  SIH_PROBLEM_ID: string;
  CONTACT_EMAIL: string;
  MOBILE: string;
}

export const identityConfig: IdentityConfig = {
  PROJECT_NAME: "SATQUERY AI",
  TAGLINE: "Agentic Multimodal Intelligence for Satellite Imagery",
  DEVELOPED_BY: "Sanjai",
  DEVELOPER_ROLE: "Full Stack Developer",
  COLLEGE_NAME: "Rajalakshmi Engineering College",
  DEPARTMENT: "Artificial Intelligence and Data Science",
  TEAM_NAME: "404 Coders",
  SIH_PROBLEM_ID: "SIH26167",
  CONTACT_EMAIL: "sanjai.e.2024.aids@rajalakshmi.edu.in",
  MOBILE: "9363574290",
  TEAM_MEMBERS: [
    {
      name: "Sanjai",
      role: "Full Stack Developer",
      skills: ["Full Stack Architecture", "Next.js & FastAPI", "System Integration"]
    },
    {
      name: "Sanjay Kumar",
      role: "AI/ML & Model Integration Lead",
      skills: ["Florence-2 LoRA", "Model Routing", "Confidence Calibration"]
    },
    {
      name: "Saqlain",
      role: "Backend & AI Systems Engineer",
      skills: ["FastAPI Systems", "Async Pipelines", "PyTorch Serving"]
    },
    {
      name: "Prathesha",
      role: "Frontend & UI/UX Engineer",
      skills: ["Next.js 14", "Spatial Visualization", "Glassmorphism UI"]
    },
    {
      name: "Sujit",
      role: "Testing, Deployment & Documentation Engineer",
      skills: ["Integration Testing", "Report Engines", "CI/CD Deployment"]
    },
    {
      name: "Saravana",
      role: "Computer Vision & Geospatial Analysis Engineer",
      skills: ["Optical-SAR Fusion", "Change Detection", "Rasterio Metadata"]
    }
  ]
};
