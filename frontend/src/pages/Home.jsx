import React, { useState } from 'react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { toast } from 'sonner';
import axios from 'axios';
import Logo from '../components/Logo';
import TechStackCategorized from '../components/TechStackCategorized';
import {
  ArrowRight,
  CheckCircle2,
  Code2,
  Database,
  FileText,
  Workflow,
  Layers,
  MessageSquare,
  Phone,
  Mail,
  Zap
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    message: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API}/contact`, formData);
      toast.success("Mensaje enviado", {
        description: "Gracias por contactarme. Te responderé pronto.",
      });
      setFormData({ name: '', email: '', company: '', message: '' });
    } catch (error) {
      console.error('Error sending contact message:', error);
      toast.error("Error al enviar", {
        description: "No se pudo enviar el mensaje. Intenta nuevamente.",
      });
    }
  };

  const whatsappNumber = "+593997154016";
  const whatsappMessage = "Hola, me interesa conocer más sobre los servicios de integración de sistemas.";
  const whatsappLink = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(whatsappMessage)}`;

  const services = [
    {
      icon: <Layers className="w-8 h-8" />,
      title: "Integración de Sistemas",
      description: "Conecta tus sistemas internos o POS con Odoo, Datil, Contifico y otras plataformas mediante APIs robustas y escalables."
    },
    {
      icon: <FileText className="w-8 h-8" />,
      title: "Facturación Electrónica",
      description: "Implementación completa de facturación electrónica cumpliendo con la normativa ecuatoriana del SRI."
    },
    {
      icon: <Code2 className="w-8 h-8" />,
      title: "Desarrollo Web a Medida",
      description: "Aplicaciones web personalizadas para operaciones internas o plataformas de negocio con tecnologías modernas."
    },
    {
      icon: <Workflow className="w-8 h-8" />,
      title: "Automatización con IA",
      description: "Automatiza flujos de trabajo complejos y crea agentes inteligentes usando n8n y tecnologías de IA."
    },
    {
      icon: <Database className="w-8 h-8" />,
      title: "Consultoría Técnica",
      description: "Asesoría especializada en arquitectura de software, optimización de procesos y selección de tecnologías."
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Optimización de Procesos",
      description: "Análisis y mejora de procesos empresariales mediante soluciones tecnológicas eficientes y escalables."
    }
  ];

  const process = [
    {
      number: "01",
      title: "Análisis",
      description: "Evaluación detallada de procesos y necesidades del negocio"
    },
    {
      number: "02",
      title: "Diseño",
      description: "Arquitectura de solución y definición de alcance técnico"
    },
    {
      number: "03",
      title: "Implementación",
      description: "Desarrollo, integración y pruebas exhaustivas"
    },
    {
      number: "04",
      title: "Soporte",
      description: "Acompañamiento continuo y optimización del sistema"
    }
  ];

  const technologies = [
    { category: "Frontend", items: ["Next.js", "React", "Tailwind CSS", "shadcn/ui"] },
    { category: "Backend", items: ["Node.js", "NestJS", "FastAPI", "Python"] },
    { category: "Automatización", items: ["n8n", "Workflows", "Integraciones"] },
    { category: "Bases de Datos", items: ["PostgreSQL", "MongoDB"] },
    { category: "ERP y Facturación", items: ["Odoo", "Datil", "Contifico"] },
    { category: "Infraestructura", items: ["Vercel", "DigitalOcean", "Docker"] }
  ];

  const cases = [
    {
      title: "Empresa Exportadora de Banano",
      description: "Sistema de gestión documental y monitoreo de contenedores en tiempo real",
      result: "Reducción del 60% en tiempo de procesamiento de documentos",
      logo: "🍌"
    },
    {
      title: "Proveedor de Servicios Web",
      description: "Automatización completa: compra, pago con tarjeta, activación de servicios e integración con ERP",
      result: "Procesamiento automático del 95% de las transacciones",
      logo: "🌐"
    },
    {
      title: "Proveedor de Dominios",
      description: "Consultoría y asesoría técnica especializada en arquitectura de sistemas",
      result: "Optimización de infraestructura y reducción de costos operativos",
      logo: "🔧"
    },
    {
      title: "Empresa de Logística",
      description: "Integración de sistemas de tracking y facturación electrónica con ERP",
      result: "Mejora del 80% en visibilidad de operaciones",
      logo: "📦"
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b border-gray-200 z-50">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-3">
          <div className="flex justify-between items-center">
            <Logo width={220} height={65} />
            <nav className="hidden md:flex gap-8 items-center">
              <a href="#servicios" className="text-gray-600 hover:text-blue-600 transition-colors font-medium">Servicios</a>
              <a href="#proceso" className="text-gray-600 hover:text-blue-600 transition-colors font-medium">Proceso</a>
              <a href="#casos" className="text-gray-600 hover:text-blue-600 transition-colors font-medium">Casos</a>
              <a href="#contacto" className="text-gray-600 hover:text-blue-600 transition-colors font-medium">Contacto</a>
            </nav>
            <Button
              onClick={() => document.getElementById('contacto').scrollIntoView({ behavior: 'smooth' })}
              className="bg-blue-600 hover:bg-blue-700 text-white"
            >
              <MessageSquare className="w-4 h-4 mr-2" />
              Contáctame
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="inline-block">
                <span className="text-sm font-semibold text-blue-600 tracking-wide uppercase">Integración de Sistemas</span>
              </div>
              <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
                Automatiza procesos y conecta tus sistemas críticos
              </h1>
              <p className="text-xl text-gray-600 leading-relaxed">
                Especialista en integración de ERP, facturación electrónica y desarrollo de soluciones empresariales para Ecuador.
              </p>
            </div>
            <div className="relative">
              <div className="aspect-square rounded-2xl overflow-hidden shadow-2xl">
                <img
                  src="https://images.unsplash.com/photo-1521737711867-e3b97375f902"
                  alt="Equipo de desarrollo profesional"
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="absolute -bottom-6 -left-6 bg-white p-6 rounded-xl shadow-xl border border-gray-100">
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="w-8 h-8 text-blue-600" />
                  <div>
                    <div className="font-semibold text-gray-900">+15 años</div>
                    <div className="text-sm text-gray-600">de experiencia</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section id="servicios" className="py-20 px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-sm font-semibold text-blue-600 tracking-wide uppercase">Servicios</span>
            <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mt-4 mb-4">
              Soluciones empresariales completas
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Desde la integración de sistemas hasta la automatización con IA
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {services.map((service, index) => (
              <Card key={index} className="border-2 border-gray-100 hover:border-blue-600 hover:shadow-lg transition-all duration-300">
                <CardHeader>
                  <div className="w-16 h-16 bg-blue-50 rounded-lg flex items-center justify-center text-blue-600 mb-4">
                    {service.icon}
                  </div>
                  <CardTitle className="text-xl">{service.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base text-gray-600">
                    {service.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Process Section */}
      <section id="proceso" className="py-20 px-6 lg:px-8 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-sm font-semibold text-blue-600 tracking-wide uppercase">Metodología</span>
            <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mt-4 mb-4">
              Cómo trabajo
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Un proceso estructurado y profesional para garantizar resultados
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {process.map((step, index) => (
              <div key={index} className="relative">
                <div className="text-6xl font-bold text-blue-100 mb-4">{step.number}</div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">{step.title}</h3>
                <p className="text-gray-600">{step.description}</p>
                {index < process.length - 1 && (
                  <div className="hidden lg:block absolute top-8 -right-4 text-blue-300">
                    <ArrowRight className="w-8 h-8" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technologies Section */}
      <section className="py-20 px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-sm font-semibold text-blue-600 tracking-wide uppercase">Stack Tecnológico</span>
            <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mt-4 mb-4">
              Tecnologías y herramientas
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Experiencia con tecnologías modernas y herramientas empresariales
            </p>
          </div>
          <TechStackCategorized />
        </div>
      </section>

      {/* Cases Section */}
      <section id="casos" className="py-20 px-6 lg:px-8 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-sm font-semibold text-blue-600 tracking-wide uppercase">Casos de Éxito</span>
            <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mt-4 mb-4">
              Proyectos reales, resultados medibles
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Soluciones implementadas para empresas ecuatorianas
            </p>
          </div>
          <div className="grid lg:grid-cols-2 gap-8">
            {cases.map((caseItem, index) => (
              <Card key={index} className="border-2 border-gray-100 hover:shadow-xl transition-shadow overflow-hidden">
                <CardHeader>
                  <div className="flex items-start gap-4">
                    <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-700 rounded-xl flex items-center justify-center text-3xl flex-shrink-0 shadow-lg">
                      {caseItem.logo}
                    </div>
                    <div className="flex-1">
                      <CardTitle className="text-xl text-gray-900 mb-2">{caseItem.title}</CardTitle>
                      <CardDescription className="text-base text-gray-600">
                        {caseItem.description}
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex items-start gap-3 bg-blue-50 p-4 rounded-lg">
                    <CheckCircle2 className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-gray-700 font-medium">{caseItem.result}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contacto" className="py-20 px-6 lg:px-8 bg-white">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-sm font-semibold text-blue-600 tracking-wide uppercase">Contacto</span>
            <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mt-4 mb-4">
              ¿Utilizas ERP o facturación electrónica?
            </h2>
            <p className="text-xl text-gray-600">
              Conversemos sobre cómo optimizar tus procesos y sistemas
            </p>
          </div>
          <Card className="border-2 border-gray-200">
            <CardContent className="p-8">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-700">Nombre completo</label>
                    <Input
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      placeholder="Tu nombre"
                      required
                      className="border-gray-300"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-700">Email</label>
                    <Input
                      name="email"
                      type="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      placeholder="tu@email.com"
                      required
                      className="border-gray-300"
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700">Empresa</label>
                  <Input
                    name="company"
                    value={formData.company}
                    onChange={handleInputChange}
                    placeholder="Nombre de tu empresa"
                    className="border-gray-300"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700">Mensaje</label>
                  <Textarea
                    name="message"
                    value={formData.message}
                    onChange={handleInputChange}
                    placeholder="Cuéntame sobre tu proyecto o necesidad..."
                    rows={5}
                    required
                    className="border-gray-300"
                  />
                </div>
                <div className="flex flex-col sm:flex-row gap-4">
                  <Button
                    type="submit"
                    size="lg"
                    className="flex-1 bg-blue-600 hover:bg-blue-700 text-white"
                  >
                    <Mail className="w-5 h-5 mr-2" />
                    Enviar mensaje
                  </Button>
                  <Button
                    type="button"
                    onClick={() => window.open(whatsappLink, '_blank')}
                    size="lg"
                    variant="outline"
                    className="flex-1 border-2 border-blue-600 text-blue-600 hover:bg-blue-50"
                  >
                    <MessageSquare className="w-5 h-5 mr-2" />
                    Escribir por WhatsApp
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-12 px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8 mb-8">
            <div>
              <Logo width={180} height={50} className="mb-4 brightness-0 invert opacity-80" />
              <p className="text-gray-400">
                Integración de sistemas y desarrollo de soluciones empresariales en Ecuador.
              </p>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Servicios</h3>
              <ul className="space-y-2 text-gray-400">
                <li>Integración de Sistemas</li>
                <li>Facturación Electrónica</li>
                <li>Desarrollo Web</li>
                <li>Automatización con IA</li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Contacto</h3>
              <ul className="space-y-2 text-gray-400">
                <li className="flex items-center gap-2">
                  <Mail className="w-4 h-4" />
                  contacto@j2systems.com
                </li>
                <li className="flex items-center gap-2">
                  <MessageSquare className="w-4 h-4" />
                  WhatsApp: +593 997 154 016
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-center text-gray-500">
            <p>&copy; 2025 J2Systems. Todos los derechos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;