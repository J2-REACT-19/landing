import { z } from "zod";

export const contactSchema = z.object({
  name: z.string().min(1, "El nombre es requerido").max(200),
  email: z.string().email("Email inválido"),
  company: z.string().max(200).optional(),
  message: z.string().min(10, "El mensaje debe tener al menos 10 caracteres").max(2000),
});

export type ContactFormData = z.infer<typeof contactSchema>;