#!/usr/bin/env python3
"""
Test script for AI services.
Run this to verify that your AI services are configured correctly.
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from app.services.ai_service_manager import AIServiceManager

load_dotenv()


async def test_service(service_name: str, manager: AIServiceManager) -> bool:
    """Test a specific AI service."""
    print(f"\n🧪 Testing {service_name.upper()} service...")

    try:
        success = manager.switch_service(service_name)
        if not success:
            print(f"❌ Failed to switch to {service_name} service")
            return False

        service = manager.get_service()
        response, conv_id = await service.process_message(
            "Hello! This is a test message. Please respond briefly."
        )

        print(f"✅ {service_name.upper()} service working!")
        print(f"   Response: {response[:100]}...")
        print(f"   Conversation ID: {conv_id[:8]}...")
        return True

    except Exception as e:
        print(f"❌ {service_name.upper()} service failed: {str(e)}")
        return False


async def main():
    """Main test function."""
    print("🤖 AI Services Test Suite")
    print("=" * 50)

    manager = AIServiceManager()

    # Check available services
    available_services = manager.get_available_services()
    print(f"📋 Available services: {', '.join(available_services)}")

    # Test each available service
    results = {}
    for service_name in ["openai", "gemini", "anthropic", "dummy"]:
        if service_name in available_services:
            results[service_name] = await test_service(service_name, manager)
        else:
            print(
                f"\n⏭️  Skipping {service_name.upper()} (no API key configured)"
            )
            results[service_name] = None

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")

    working_services = []
    for service, result in results.items():
        if result is True:
            print(f"  ✅ {service.upper()}: Working")
            working_services.append(service)
        elif result is False:
            print(f"  ❌ {service.upper()}: Failed")
        else:
            print(f"  ⏭️  {service.upper()}: Skipped (not configured)")

    if working_services:
        print(f"\n🎉 {len(working_services)} service(s) working correctly!")
        print("🚀 Your AI Agent app is ready to use!")
    else:
        print(
            "\n⚠️  No AI services are working. Check your API keys and configuration."
        )

    # Show configuration tips
    if "openai" not in working_services and "openai" in available_services:
        print("\n💡 OpenAI Tips:")
        print("   - Verify OPENAI_API_KEY in your .env file")
        print("   - Check your OpenAI account has credits")

    if "gemini" not in working_services and "gemini" in available_services:
        print("\n💡 Gemini Tips:")
        print("   - Verify GEMINI_API_KEY in your .env file")
        print("   - Ensure the API key has Gemini API access")

    if (
        "anthropic" not in working_services
        and "anthropic" in available_services
    ):
        print("\n💡 Anthropic Tips:")
        print("   - Verify ANTHROPIC_API_KEY in your .env file")
        print("   - Check your Anthropic account has credits")


if __name__ == "__main__":
    asyncio.run(main())
