# HealthBuddy - Comprehensive Health Assistant

## Overview

HealthBuddy has been enhanced from a fitness-only assistant to a **comprehensive health guide** covering all health perspectives. It now provides guidance on fitness, nutrition, mental health, sleep, hydration, and disease prevention.

## What's New

### 1. Expanded Knowledge Base

Added comprehensive health guides:

**Mental Health Guide**
- Basics of mental health
- Common mental health conditions (anxiety, depression, stress, burnout, PTSD)
- Stress management techniques
- Mindfulness practices
- Building resilience
- When to seek professional help
- Healthy lifestyle for mental health
- Work-life balance

**Sleep Health Guide**
- Importance of sleep
- Sleep cycles and stages
- Better sleep hygiene
- Common sleep disorders
- Natural sleep aids
- Sleep and productivity
- Sleep tracking
- Sleep recommendations by age

**Disease Prevention Guide**
- Basic prevention principles
- Cardiovascular health
- Diabetes prevention
- Cancer prevention
- Infectious disease prevention
- Immune system support
- Hygiene practices
- Screening guidelines
- Warning signs to watch

**Hydration Guide**
- Importance of hydration
- Daily water intake recommendations
- Signs of dehydration
- Hydration for exercise
- Best fluids for hydration
- Hydration myths
- Hydration by activity level
- Hydration for special conditions

### 2. New Health Calculators

**Water Intake Calculator**
- Calculates daily water needs based on weight
- Adjusts for activity level (sedentary, light, moderate, heavy)
- Provides recommendations in liters, ml, and glasses

**Sleep Calculator**
- Calculates recommended sleep duration based on age
- Covers all age groups from newborns to older adults
- Provides age-specific sleep recommendations

**Heart Rate Calculator**
- Calculates maximum heart rate
- Determines target heart rate zones
- Supports different exercise intensities (light, moderate, vigorous)

### 3. Enhanced Simple FitBuddy (No API Key Required)

The no-API-key version now includes:
- All original fitness tools (BMI, calories, meal plans)
- New hydration calculator
- New sleep calculator
- New heart rate calculator
- Expanded knowledge base search
- Web search for health information

### 4. Rebranding

Renamed from "FitBuddy" to "HealthBuddy" to reflect the comprehensive health coverage.

## Usage

### Run Simple HealthBuddy (No API Key)

```bash
python simple_fitbuddy.py
```

Menu options:
1. Calculate BMI
2. Calculate Daily Calories
3. Calculate Meal Plan Calories
4. Calculate Water Intake Needs
5. Calculate Sleep Requirements
6. Calculate Target Heart Rate
7. Search Health Knowledge Base
8. Web Search for Health Info
9. Exit

### Run AI Agent Version (Requires OpenAI API Key)

```bash
python main.py
```

The AI agent version provides:
- Natural language conversation
- Multi-step reasoning
- Automatic tool selection
- Context-aware responses

## Health Perspectives Covered

### 1. Physical Health
- Fitness and exercise
- Nutrition and diet
- BMI and weight management
- Hydration
- Sleep quality

### 2. Mental Health
- Stress management
- Mindfulness and meditation
- Emotional well-being
- Building resilience
- Work-life balance

### 3. Preventive Health
- Disease prevention
- Screening guidelines
- Immune system support
- Hygiene practices
- Warning signs

### 4. Lifestyle Health
- Daily routines
- Habit formation
- Sleep hygiene
- Hydration habits
- Activity levels

## Technical Architecture

The system maintains the original architecture with enhanced components:

- **RAG System**: Now searches 6 comprehensive health guides
- **Tools**: 7 health calculators (up from 4)
- **Knowledge Base**: 4x more content coverage
- **Web Search**: Health-focused queries

## Future Enhancements

Potential additions:
- Symptom checker (with appropriate disclaimers)
- Medication information (with safety warnings)
- Emergency health guidance
- Personal health profiles
- Progress tracking
- Health goal setting
- Integration with health devices

## Important Notes

1. **Not Medical Advice**: HealthBuddy provides general health information, not medical advice. Always consult healthcare professionals for medical concerns.

2. **Emergency Situations**: HealthBuddy is not designed for emergency situations. Call emergency services for urgent medical needs.

3. **Professional Consultation**: For serious health concerns, always consult qualified healthcare professionals.

4. **Disclaimer**: HealthBuddy is an educational tool and should not replace professional medical advice.

## Documentation

- **README.md**: Full project documentation
- **ARCHITECTURE.md**: Technical architecture details
- **QUICKSTART.md**: Quick start guide
- **GROQ_SETUP.md**: Groq API setup (if using Groq)
- **HEALTH_GUIDE.md**: This document

## Conclusion

HealthBuddy now provides comprehensive health guidance across all major health perspectives, making it a complete health assistant for wellness, fitness, nutrition, mental health, and preventive care.
